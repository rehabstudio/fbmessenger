# FB Messenger demo

Create a FB app and page for your bot (follow the instructions in the fbmessenger readme)

Assuming you are using [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
 
 	mkdir messenger-demo
 	cd messenger-demo
 	mkvirtualenv -a . messenger-demo
 	
Edit your `postactivate` file which will be in a location similar to `~/.virtualenvs/messenger-demo/bin/postactivate`

Add the following environment variables

	export FB_PAGE_TOKEN=<YOUR_FB_PAGE_TOKEN>
	export FB_VERIFY_TOKEN=<YOUR_ FB_VERIFY_TOKEN>

Run the app

	python main.py
	
You can deploy this to a server or use [ngrok](https://ngrok.com/) to proxy Facebok requests to your localhost for testing

To setup the bot hit the follwing url in a browser

	https://<YOUR_DOMAIN>/webhook?hub.verify_token=<YOUR_ FB_VERIFY_TOKEN>&init=true
	
Set your Messenger app webhook to
	
	https://<YOUR_DOMAIN>/webhook
