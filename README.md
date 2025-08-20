# Full-Stack To-Do List Application

This project is a simple full-stack to-do list application with a React frontend and a Node.js/Express backend.

## Project Structure

- `client/`: Contains the React frontend application.
- `server/`: Contains the Node.js/Express backend server.

## Getting Started

To get the application running on your local machine, follow these steps.

### Prerequisites

- Node.js and npm installed on your machine.

### Installation

1.  **Install backend dependencies:**
    Navigate to the `server` directory and install the required packages.

    ```bash
    cd server
    npm install
    ```

2.  **Install frontend dependencies:**
    Navigate to the `client` directory and install the required packages.

    ```bash
    cd ../client
    npm install
    ```

### Running the Application

You need to run both the backend and frontend servers in separate terminals.

1.  **Run the backend server:**
    In the `server` directory, run the following command:

    ```bash
    node index.js
    ```

    The server will start on `http://localhost:3001`.

2.  **Run the frontend application:**
    In the `client` directory, run the following command:

    ```bash
    npm start
    ```

    The React development server will start, and the application will open in your browser at `http://localhost:3000`.

## How to Use

-   View your to-do list.
-   Add new to-dos using the input field.
-   Delete to-dos by clicking the "Delete" button.

## Deployment

This application is composed of two parts: a React frontend and a Node.js backend, which need to be deployed separately.

### Frontend (Client)

The React application is a static site. You can host it on any static site hosting service. Popular choices include Netlify, Vercel, and GitHub Pages.

**General Steps for Netlify/Vercel:**

1.  Push the code to a GitHub repository.
2.  Sign up for Netlify or Vercel and connect your GitHub account.
3.  Create a new project/site and select the repository.
4.  Configure the build settings:
    -   **Build Command:** `npm run build` or `react-scripts build`
    -   **Publish Directory:** `client/build`
    -   **Base Directory:** `client` (or leave blank if the service detects it)
5.  You will also need to set an environment variable for the frontend to know where the backend API is. For example:
    -   `REACT_APP_API_URL=https://your-backend-api-url.com`
    You would then need to update the `App.js` to use `process.env.REACT_APP_API_URL` instead of a hardcoded `http://localhost:3001`.

### Backend (Server)

The Node.js backend is a dynamic application that needs to be hosted on a service that can run Node.js code, such as Render, Heroku, or a virtual private server (VPS).

**General Steps for Render/Heroku:**

1.  Push the code to a GitHub repository.
2.  Sign up for Render or Heroku and connect your GitHub account.
3.  Create a new Web Service/App and select the repository.
4.  Configure the service:
    -   **Root Directory:** `server`
    -   **Build Command:** `npm install`
    -   **Start Command:** `node index.js`
5.  The service will provide you with a public URL for your backend API. Use this URL for the `REACT_APP_API_URL` environment variable in your frontend deployment.
6.  Ensure your `server/index.js` uses `process.env.PORT` for the port number, as the hosting service will provide this. Our code already does this.
