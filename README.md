# Matterport Flask Server

A Flask server inspired by the [matterport-dl](https://github.com/rebane2001/matterport-dl) project, designed to host downloaded matterport models online!

## Features

- Hosts 3D models downloaded using the `matterport-dl` tool.
- Provides a clean and customizable frontend to showcase and access models.
- Supports local and Heroku deployments with Amazon S3 integration for cloud hosting.

---

## Setup and Usage

### Prerequisites
1. Download your models using `matterport-dl` by following its instructions [here](https://github.com/rebane2001/matterport-dl).
2. Get ready to see the worst code ever.

---

### Step 1: Download Models
1. Use `matterport-dl` to download the models.
2. Keep the default save location as it creates two essential folders:
   - `downloads`
   - `graph_posts`

   **Do not change the folder structure if you don't like touching the code.**

---

### Step 2: Configure `index.html`
1. Open `index.html` in the project directory.
2. Add the IDs of your models to the `<a>` tags for each card instead of '11wordsid11'.
3. (optional) Add an image for the card
Here's an example:

```html
<div class="card">
    <a href="/11wordsid11/"></a>
    <img src="https://via.placeholder.com/400x300" alt="Card 1">
    <div class="card-overlay">Name to Display</div>
</div>
```

Will turn to:
```html
<div class="card">
    <a href="/roWLLMMmPL8/"></a>
    <img src="https://upload.wikimedia.org/wikipedia/commons/f/fc/Deras-TreeHouse.JPG" alt="Card 1">
    <div class="card-overlay">Name to Display</div>
</div>
```

- Replace `11wordsid11` with the ID of your model.
- Update `alt` and `Name to Display` for a custom description.

---

### Step 3: Deployment Options

#### Option 1: Deploy on your own server
1. Place the `downloads` and `graph_posts` folders in the project's root directory (next to `app.py`).
2. Run the Flask app:

```bash
python app.py
```

3. Your app should be running on localhost:5000, expose that port and you should be able to access it from anywhere

---

#### Option 2: Deploy on Heroku with Amazon S3
1. Upload the `downloads` folder to an Amazon S3 bucket:
   - Ensure public access is enabled for the uploaded files.
   - Update your bucket's policy as required.
2. Edit the `app-s3.py` file:
   - Set the `BASE_DIR_ORG` variable to your S3 bucket URL:
     ```python
     BASE_DIR_ORG = 'https://bucket-name.s3.amazonaws.com/downloads/'
     ```
3. Rename `app-s3.py` to `app.py`, and delete the original `app.py`.
4. Push the project to Heroku:
   ```bash
   git add .
   git commit -m "Deploying to Heroku"
   git push heroku main
   ```
5. Your app is now live on Heroku!

---

## Notes
- Make sure all files are correctly placed as per the instructions.
- For Heroku deployments, ensure your S3 bucket is configured for public access to avoid 403 errors.

---

## Acknowledgments
- This project is simply a derivative of what the masterminds behind [matterport-dl](https://github.com/rebane2001/matterport-dl) project have done, Thanks.
- Thanks to (Venice Project Center)[https://veniceprojectcenter.org] who were looking to safekeep their models and kick started the idea.
- Thanks to (Matterport)[https://matterport.com] for their awesome technology and horrible subscription model

---

## License
This project is licensed under the MIT License. See the LICENSE file for details.

