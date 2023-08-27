# flask_p5_minimal
Minimal example project for hosting p5 sketches locally with python (flask). This branch includes a websocket backend to demonstrate transferring data to/from the p5.js frontend, and persisting state data across connected clients.

https://p5js.org/
https://github.com/abachman/p5.websocket

https://flask.palletsprojects.com/en/2.0.x/

# running
If just running to test on local machine, simply run the python file and go to http://127.0.0.1:8000

If testing on local network, set app host to 0.0.0.0, e.g. app.run(host='0.0.0.0'), then navigate to the IP address of the host machine, e.g. if your PC's IP is 192.168.1.1, you could access the hosted page by navigating to http://192.168.1.1:8000 on your phone.
