# FaceRecognition

A working implementation of the face recognition application developed on top of the **face_recognition** library.

Please refer to this github link for more information: https://github.com/ageitgey/face_recognition.

For setting the development environment, it is recommended to use the dockerfile provided to build and setup everything.</br>
Mount the volume (code directory) to the container and you're ready to go.</br>

```
docker run --name <your_container_name> -e HOST_IP=$(ifconfig en0 | awk '/ *inet /{print $2}') -v <code_dir>:/app -t -i <image_name>:latest /bin/bash
```

# .env variables
**SECRET_KEY** = (str) secret_key_to_use </br>
**DEBUG** = (bool) </br>
**PORT** = (int) </br>
**HOST** = (str) IP/URL

Application uses pipenv so be sure to enter the pip environment first. ```pipenv shell```</br>
To run the application: ```python server.py```

# This does not support text recognition.

# Using the application
After running the server go to the URL you have used in the .env file.</br>
For now, it only supports JSON inputs.</br>

*Sample input*
```
{
	"id_picture": "https://cdn-images-1.medium.com/max/1600/1*GSBmboEShxfUQFBgI_BGTA.jpeg",
	"selfie": "https://cdn-images-1.medium.com/max/1600/1*GSBmboEShxfUQFBgI_BGTA.jpeg"
}
```
It will return a boolean response.</br>
**True** if the face(s) match</br>
**False** if the face(s) did not match, image is too blur to process or no face image found in one or both images provided.

It will also throw other responses which are handled exceptions:
```
{
	"message": "<error message>"
}
```

Thanks to [ageitgey](https://github.com/ageitgey) for providing such useful library and all the contributors and inspirations.
