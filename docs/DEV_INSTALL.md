# Running the App with Docker
If you would like to help with development please reach out [here on the Grey-Box webiste](https://www.grey-box.ca/contact/).

## 🛠️ For Development

### 📥 Step 1: Clone the Repository

Start by cloning this repository to your local machine:

```shell
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```
Make sure you're in the root of the repo—this is where the compose.yaml file lives.


### 🐳 Step 2: Install Docker Desktop (if needed)

We recommend using Docker Desktop (which includes Docker Compose) to run the app locally.

👉 Follow the official instructions to install Docker Desktop or just the Compose plugin:  
[📦 Install Docker Desktop / Docker Compose](https://docs.docker.com/compose/install/)
<hr>

## 🚀 App Startup

>Run these commands from the root of the repo where the compose.yaml file is located. 

To start the app for development run:

```shell
docker compose up --build --watch
```

This will:
- Build the container according to the `Dockerfile`
- Start the app in the container and watch your source files for changes.
- Rebuild application and restart Uvicorn on file updates.

⚠️ Ensure the UVICORN_RELOAD environment variable is set in your .env file so Uvicorn restarts automatically when you update files.

The `--watch` option watches the source code for changes and rebuilds/refreshes containers when files are updated. Watch can then be enabled/disabled in the terminal to toggle this feature on and off. If you are making a large number of changes, it might be good to toggle it off until you need it to update, otherwise it will sync and rebuild/redeploy when you stop typing.

### 🧪 Alternative Startup (Manual Build & Watch)
You can also run the two commands separately to achieve the same result:
```shell
docker compose up --build -d
docker compose watch
```
- The `-d` option starts the container in the background.

## 🛑 App Shutdown
To stop the application press `Ctrl+C` and run:

```shell
docker compose down
``` 
To also clean up local Docker images and free up disk space:
```shell
docker compose down --rmi local
```
This removes:
- The container
- The codex network generated to access the API endpoints. 
- (Optional) Local images build for development.

You can manually remove them via CLI or the Docker Desktop app.



