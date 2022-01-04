# protected-by-ring

This instillation art piece aimed to bring awareness to Amazon products’ data collection (specifically the Ring doorbell). The average consumer believes that surveillance data—such as the images collected by the Ring doorbell—has little-to-no value. To challenge this mentality, we used a machine learning model to render Ring doorbell surveillance images in the style of famous artwork. Thus, our exhibit displays Ring doorbell images as priceless works of art.

This project utilizes the ring_doorbell api to interact with a Ring doorbell. When a user presses the doorbell, an image is downloaded from the Ring doorbell. Face cropping is then attempted. After, the image goes through style transfer via the STROTTS (https://arxiv.org/abs/1904.12785) model, the final results of which can be seen below:

Content image:![main_portrait](https://user-images.githubusercontent.com/43860983/148039935-42858077-1625-4172-ad19-3f4392cd6a34.png)

![scene_me](https://user-images.githubusercontent.com/43860983/148039535-ebbacb22-787c-4f9b-ba17-db194bc51a01.jpg)

Style image:
![style](https://user-images.githubusercontent.com/43860983/148039661-c1b628c6-e537-4324-8160-716d5ecc7301.jpg)

Result:
![main_portrait](https://user-images.githubusercontent.com/43860983/148039959-87f5a744-5c81-4a67-89b0-649b01eb9565.png)

