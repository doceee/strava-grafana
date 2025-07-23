# Strava Grafana

This project allows you to fetch activities from Strava, store them in a MySQL database, and visualize the data in Grafana.

## Requirements

- Docker and Docker Compose
- Strava account with generated API credentials
- Required environment variables (the `.env` file)

## Setup

1. **Create a `.env` file in the project root** and fill it with the following variables:

   ```
   STRAVA_CLIENT_ID=your_client_id
   STRAVA_CLIENT_SECRET=your_client_secret
   STRAVA_REFRESH_TOKEN=your_refresh_token

   MYSQL_HOST=db
   MYSQL_PORT=3306
   MYSQL_USER=root
   MYSQL_PASSWORD=your_password
   MYSQL_DATABASE=strava
   ```

2. **Start the services using Docker Compose:**

   ```
   docker-compose up -d
   ```

   - This will start the MySQL database and Grafana.
   - Grafana will be available at: [http://localhost:3000](http://localhost:3000)
   - Default Grafana login: `admin` / `admin`

3. **Import data from Strava into the database:**

   After the database container is running, run the following commands locally:

   ```
   pip install -r requirements.txt
   python seed.py
   ```

   The script will fetch your activities from Strava and save them to the MySQL database.

4. **Grafana Dashboards:**

   - Dashboards are automatically provisioned from the `grafana/dashboards` directory.
   - After logging into Grafana, you will find a ready-to-use dashboard for activity visualization.

## Project Structure

- `docker-compose.yml` – Docker services configuration (MySQL, Grafana)
- `seed.py` – script for fetching and saving Strava activities to MySQL
- `grafana/` – Grafana configuration and dashboards

## Notes

- If you don't have a `requirements.txt` file, install the required libraries manually:
  ```
  pip install mysql-connector-python requests python-dotenv
  ```
- Make sure your Strava API credentials are correct and have the necessary permissions.
- The `seed.py` script automatically checks for all required environment variables and handles errors gracefully. If any variable is missing or an error occurs (e.g., connection issues, API errors), the script will print a clear error message and stop execution.
