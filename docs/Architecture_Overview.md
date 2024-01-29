# Architecture Overview
## Components
The system is composed of three main components, each serving a distinct role in the overall architecture:
### Frontend
The frontend component encompasses the user interface and interaction layer of the application. In the initial implementation, the frontend is developed using Django templates to render dynamic content on the server side. Future plans involve the integration of Vue.js for enhanced client-side interactivity.
- #### Technologies Used
    - Django Templates (current)
    - Vue.js (planned)

- Interactions
    - Communicates with the backend via HTTP requests to fetch and update data.
    - Renders dynamic content based on server-side template

### Backend
The backend component is responsible for managing the server-side logic, databases, and APIs. Django, a high-level Python web framework, is utilized to handle HTTP requests, process business logic, and interact with the PostgreSQL database. Additionally, Pandas and Matplotlib is used for creating and rendering charts within the application. This component contributes to visualizing data insights and trends.

- #### Technologies Used
    - Django Framework: Version 4.2.5
    - Django Rest Framework: 3.14.0 (For future implementation of the API)
    - Python: Backend logic is implemented using Python.
    - PostgreSQL: Database management system for data storage.
    - Pandas(2.0.3), Matplotlib(3.7.3): Used for creating and rendering charts 

- Interactions
    - Handles incoming HTTP requests from the frontend.
    - Implements business logic and interacts with the database.
    - Provides APIs for data exchange with the frontend.

### Database
The Database component manages the structure and organization of the data layer. PostgreSQL is employed to store and retrieve data related to user accounts, purchases, supplier information, and other entities. The data folder contains initial CSV files used for data seeding.

- #### Technologies Used
    - PostgreSQL: Version [15]

- #### Organization
    Stores tables for orders,expenses,products,supplier information, and other relevant entities. Ensures data integrity and consistency through relational database principles.



## Data Flow
 The data flow within the system involves several stages, from user input to data storage and retrieval. 
 
 The illustration below outlines the primary steps and interactions:
- **User Interaction on Frontend**
    - Users interact with the frontend through the user interface.
    - Input data includes user registration details, purchase information, and other relevant forms.
-  **Communication with Backend**
    - Frontend components communicate with the Backend through HTTP requests.
    - Django handles incoming requests and routes them to the appropriate views.
- **Backend Processing**
    - Backend components process incoming requests and perform necessary business logic.
    - Data transformations and validations occur at this stage, ensuring the integrity and accuracy of the data.
- **Database Interaction**
        - The Backend interacts with the PostgreSQL database to store or retrieve data.
        - CRUD operations (Create, Read, Update, Delete) are executed based on user actions.
- **Chart Rendering (Matplotlib)**
        - In cases where charts are required, the Backend utilizes Matplotlib to generate visualizations.
        - Chart data may be derived from database queries or processed data.
- **Response to Frontend**
        - The Backend sends responses back to the Frontend, containing the results of user requests.
        - Responses may include success messages, data for rendering templates, or chart images.
- **Rendering on Frontend**
        - The Frontend renders dynamic content based on the received data.
        - Vue.js, when integrated, will handle client-side interactivity and dynamic updates.
- **User Feedback**
        - Users receive feedback on their actions through the rendered user interface.
        - Feedback may include success messages, error notifications, or visual representations of data.

- **Data Seeding (Optional)**
        - Initial data may be seeded into the system using CSV files or other data sources in the data folder.

### System Architecture Diagram
#### - [Architecture Diagram](/docs/Architecture_Diagram.png)

