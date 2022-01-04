import cv2
import numpy as np
from scipy.io.wavfile import read, write
import wave
import io

#declaring variables (n must be 1-8)
n = 1
in_filename = 'test_image.jpg' 
message_to_hide = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse non dolor egestas, semper ipsum non, dapibus est. Proin rutrum, est eget sagittis rutrum, tellus nulla sodales felis, ac bibendum metus tortor vel neque. Pellentesque habitant morbi tristique senectus et netus et malesuada viverra.'

#1...
#Write a function, imagehide, that takes as input an image file (e.g., a jpg) and a message,
#embedding the message in the least significant bits of the R, G, and B values for each pixel and saving
#the modified image to a new file. It should take an optional third parameter, an integer n 
#(with default value 1 if it is not provided), indicating how many bits of the message to encode per color value per pixel. 
#In other words, by default, you will embed 3 bits per pixel (1 each for R, G, and B).
def imagehide(img, message, out_filepath, n: int = 1):
	#each pixel is (r,g,b) where color values (0-255) are 8 bit values
	if isinstance(message, str):
		message = message + "*stop*"
		binary_message = ''.join(format(x, '08b') for x in bytearray(message, 'utf-8'))
	else:
		print("message must be a string")
		return

	hide_in_image = cv2.imread(img)
	curr_i = 0
	max_i = len(binary_message)
	for row in hide_in_image:
		for p in row:
			#convert to binary 
			for pixel_i in range(3):
				rgb = format(p[pixel_i], "08b")
				if (curr_i + n) <= max_i:
					#int with base = 2
					p[pixel_i] = int(rgb[:-n] + binary_message[curr_i:(curr_i+n)], 2)
					curr_i = curr_i + n

				elif curr_i < max_i:
					new_n = max_i - curr_i
					p[pixel_i] = int(rgb[:-new_n] + binary_message[curr_i:], 2)
					curr_i = curr_i + n

				elif curr_i >= max_i:
					break

	cv2.imwrite(out_filepath, hide_in_image) 

out_filename = 'hide_in_image.png'
imagehide(in_filename, message_to_hide, out_filename, n) 

#2...
#Think carefully about what image format you are using as the output of this function, 
#particularly how compression may impact your function. First, write a version, imagehidecompressed, 
#that outputs a compressed (lossy) file format, and make sure imagehide uses an uncompressed, non-lossy format. 
#Compare the least significant bits of each output after reading them in again, 
#and describe in your write-up (as "Part 1") what you observe.
def imagehidecompressed(img, message, n: int = 1):

	if isinstance(message, str):
		message = message + "*stop*"
		binary_message = ''.join(format(x, '08b') for x in bytearray(message, 'utf-8'))
	else:
		print("message must be a string")
		return

	hide_in_image = cv2.imread(img)
	curr_i = 0
	max_i = len(binary_message)
	for row in hide_in_image:
		for p in row:
			for pixel_i in range(3):
				rgb = format(p[pixel_i], "08b")
				if (curr_i + n) <= max_i:
					p[pixel_i] = int(rgb[:-n] + binary_message[curr_i:(curr_i+n)], 2)
					curr_i = curr_i + n

				elif curr_i < max_i:
					new_n = max_i - curr_i
					p[pixel_i] = int(rgb[:-new_n] + binary_message[curr_i:], 2)
					curr_i = curr_i + n

				elif curr_i >= max_i:
					break

	jpg_out_filename = 'hide_in_image.jpg'
	png_out_filename = 'hide_in_image_png_compress.png'
	cv2.imwrite(jpg_out_filename, hide_in_image, [int(cv2.IMWRITE_JPEG_QUALITY), 100]) 
	cv2.imwrite(png_out_filename, hide_in_image,  [int(cv2.IMWRITE_PNG_COMPRESSION), 9])

def compare_images(lossy, non_lossy, n):
	hidden_lossy = cv2.imread(lossy)
	hidden_non_lossy = cv2.imread(non_lossy)

	diffs = 0
	for row in range(len(hidden_lossy)):
		for col in range(len(hidden_lossy[row])):
			for pixel_i in range(3):
				rgb_lossy = format(hidden_lossy[row][col][pixel_i], "08b")
				rgb_lossy_int = int(rgb_lossy[-n:],2)
				rgb = format(hidden_non_lossy[row][col][pixel_i], "08b")
				rgb_int = int(rgb[-n:],2)

				diffs = diffs + abs(rgb_int - rgb_lossy_int)
	
	return diffs			

imagehidecompressed(in_filename, message_to_hide, n) 
img_diffs = compare_images('hide_in_image.jpg', 'hide_in_image.png', n)
print("difference between least significant bits (jpg): {} \n".format(img_diffs))
img_diffs = compare_images('hide_in_image_png_compress.png', 'hide_in_image.png', n)
print("difference between least significant bits (compressed png): {} \n".format(img_diffs))

#3...
#Then write a function, imagereveal, that takes as input an image file of the form created by imagehide 
#and optionally an integer n (with default value 1 if it is not provided). This function's output should be 
#the message encoded in Step 1. The second parameter, n, specifies that the function should use the n least 
#significant bits of each pixel value. So far, we've been assuming this is 1.
def imagereveal(img, n: int = 1):
    hidden_image = cv2.imread(img)
    hidden_message = ""

    for row in hidden_image:
        for p in row:
            for pixel_i in range(3):
            	rgb = format(p[pixel_i], "08b")
            	hidden_message = hidden_message + rgb[-n:]

    reveal_message = ""
    for i in range(0, len(hidden_message), 8):
        one_byte = hidden_message[i: i+8]
        reveal_message = reveal_message + chr(int(one_byte, 2))
        if reveal_message[-6:] == "*stop*":
            reveal_message = reveal_message[:-6]
            break

    return reveal_message

recovered = imagereveal('hide_in_image.png', n)
print("Message recovered from image: {} \n".format(recovered))

recovered_lossy = imagereveal('hide_in_image.jpg', n)
print("Message recovered from lossy image: {} \n".format(recovered_lossy))

recovered_lossy_png = imagereveal('hide_in_image_png_compress.png', n)
print("Message recovered from compressed png image: {} \n".format(recovered_lossy_png))

#4...
#Now try varying n. In your write-up, as "Part 2," describe briefly what you see. 
#Include sample image files (referenced by filename in the write-up) with different values of n.

#imagehide(in_filename, message_to_hide,'hide_in_image1.png', 1) 
imagehide(in_filename, message_to_hide, 'hide_in_image2.png', 2) 
imagehide(in_filename, message_to_hide, 'hide_in_image3.png', 3) 
imagehide(in_filename, message_to_hide, 'hide_in_image4.png', 4) 
imagehide(in_filename, message_to_hide, 'hide_in_image5.png', 5) 
imagehide(in_filename, message_to_hide, 'hide_in_image6.png', 6) 
imagehide(in_filename, message_to_hide, 'hide_in_image7.png', 7) 
imagehide(in_filename, message_to_hide, 'hide_in_image8.png', 8) 

#5...
#Finally, let's switch over to audio steganography. Repeat Steps 1 through 4 for an audio file, 
#creating functions audiohide and audioreveal analogous to the above. We won't work with compressed files, 
#but only uncompressed WAV files. In your write-up, "Part 3" should briefly discuss how the amount of data 
#you embed (the number of bits) per sample relates to whether you audibly notice modifications in the audio file.
def audiohide(wav_file, message, out_filepath, n: int = 1):

	wav_for_encode = wave.open(wav_file ,mode="rb")
	wav_to_bytes = bytearray(list(wav_for_encode.readframes(wav_for_encode.getnframes())))

	if isinstance(message, str):
		message = message + "*stop*" 
		binary_message = ''.join(format(x, '08b') for x in bytearray(message, 'utf-8'))
	else:
		print("message must be a string")
		return

	for i in range(0,len(binary_message),n):
		temp = format(wav_to_bytes[i], "08b")
		wav_to_bytes[i] = int(str(temp[:-n]) + binary_message[i:i+n], 2)

	encoded_wav = bytes(wav_to_bytes)
	save_out_wav =  wave.open(out_filepath, 'wb')
	save_out_wav.setparams(wav_for_encode.getparams())
	save_out_wav.writeframes(encoded_wav)

	save_out_wav.close()
	wav_for_encode.close()
			

def audioreveal(wav_file, n: int = 1):
	wav_for_decode = wave.open(wav_file, mode='rb')
	wav_to_bytes = bytearray(list(wav_for_decode.readframes(wav_for_decode.getnframes())))

	hidden_message = []
	for i in range(len(wav_to_bytes)):
		hidden_message.append(format(wav_to_bytes[i], "08b")[-n:])

	reveal_message = ""
	for i in range(0, len(hidden_message), 8):
		one_byte = "".join(map(str,hidden_message[i:i+8]))
		reveal_message = reveal_message + chr(int(one_byte, 2))
		if reveal_message[-6:] == "*stop*":
			reveal_message = reveal_message[:-6]
			break

	wav_for_decode.close()
	return reveal_message

out_filename = 'hide_in_wav.wav'
in_wavname = 'test.wav'
#I changed this message during testing. I used progressively longer messages up to 10000 bytes.
message_to_hide = "This is a test"

audiohide(in_wavname, message_to_hide, out_filename) 
revealed = audioreveal(out_filename)
print("Message recovered from audio: {}".format(revealed))
