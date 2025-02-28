# **Task Mania API** –
[![Checking tests](https://github.com/hagp55/task-mania/actions/workflows/test.ci.yaml/badge.svg)](https://github.com/hagp55/task-mania/actions/workflows/test.ci.yaml)
[![Check by the linter](https://github.com/hagp55/task-mania/actions/workflows/linter.ci.yaml/badge.svg)](https://github.com/hagp55/task-mania/actions/workflows/linter.ci.yaml)


## Welcome to **Task Mania API** – your reliable assistant for task and project management. Keep track of your tasks, stay organized, and never forget important things! ✅

### 🔥 **What Can You Do?**

#### 🏗 **Project Management**
- 📌 **Create & organize projects** – keep your work structured.
- 📖 **View all projects** – get a clear overview.
- ✏ **Update project details** – modify anytime.
- 🗑 **Delete unnecessary projects** – keep your workspace clean.

#### ✅ **Tasks**
- 📝 **Create tasks** – keep track of important to-dos.
- 📖 **View tasks** – always stay on top of things.
- ✏ **Update tasks** – modify as needed.
- 🗑 **Delete tasks** – clear up your task list.

#### 👤 **User Management**
- 🔹 **Register users** – create accounts easily.
- ✏️ **Change password** – change password accounts easily.
- 🔍 **View user information** – get personal info.

#### 🔐 **Authorization**
- 🔑 **Login with email and password** – the classic way.
- ✉ **Sign in with Google** – fast and convenient.
- 📨 **Sign in with Yandex** – another easy option.

---

### 🔮 **What’s Coming Next?**
✨ **Not implemented**
- 📱 **Sign in with phone number.**
- 💬 **Sign in with Telegram.**
- ⏳ **Set due dates for tasks** – schedule and manage deadlines effectively.

📌 *Stay tuned for updates! More exciting features are on the way!* 🚀

---

## API Endpoints

### Healthcheck 👨‍⚕️
- **GET `/api/v1/healthcheck`**: Get the current status of the application (Only staff).
- **GET `/api/v1/healthcheck/db`**: Check the availability of the database connection (Only staff).

### Projects 👨‍💻
- **POST `/api/v1/projects`**: Create a new project.
- **GET `/api/v1/projects`**: Get a list of all projects.
- **GET `/api/v1/projects/{project_id}`**: Get the details of a specific project.
- **PUT `/api/v1/projects/{project_id}`**: Update the details of an existing project.
- **DELETE `/api/v1/projects/{project_id}`**: Delete a specific project.

### Tasks 📆
- **POST `/api/v1/tasks`**: Create a new task.
- **GET `/api/v1/tasks`**: Get a list of all tasks.
- **GET `/api/v1/tasks/{task_id}`**: Get a specific task by its ID.
- **PUT `/api/v1/tasks/{task_id}`**: Update a task with the provided data.
- **DELETE `/api/v1/tasks/{task_id}`**: Delete a specific task.

### Users 👨‍🦱
- **POST `/api/v1/users/signup`**: Register a new user.
- **PUT `/api/v1/users/change_password`**: Change the password for a user.
- **GET `/api/v1/users/me`**: Get information about the authenticated user.

### Auth 🔐
- **POST `/api/v1/auth/login`**: Authenticate a user and get a login token.
- **GET `/api/v1/auth/login/google`**: Redirect the user to the Google authentication page for login or signup.
- **GET `/api/v1/auth/google`**: Handle the callback from Google authentication.
- **GET `/api/v1/auth/login/yandex`**: Redirect the user to Yandex authorization page for login/signup.
- **GET `/api/v1/auth/yandex`**: Handle the callback from Yandex authentication.
