# Ring Art Gallery

This instillation art piece aimed to bring awareness to Amazon products’ data collection (specifically the Ring doorbell). The average consumer believes that surveillance data has little-to-no value. To challenge this mentality, we used a machine learning model to render Ring doorbell surveillance images in the style of famous artwork. Thus, our exhibit displays Ring doorbell images as priceless works of art.

This project utilizes the ring_doorbell api to interact with a Ring doorbell. When a user presses the doorbell, an image is downloaded from the Ring doorbell. Face cropping is then attempted. After, the image goes through style transfer via the STROTTS model (https://arxiv.org/abs/1904.12785), the final results of which can be seen below:

Content image: 

![scene_me](https://user-images.githubusercontent.com/43860983/148045933-3d34090e-fd26-4c51-95cc-ec165988914d.jpg)

Style image:

![style](https://user-images.githubusercontent.com/43860983/148045948-15e067bd-5860-4224-aca0-3d71a4275624.jpg)

Result:

![main_portrait](https://user-images.githubusercontent.com/43860983/148045969-119a8025-fd4a-4165-84b8-237188c7f3d8.png)
