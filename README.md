# WebStar Analytics
🔗 **Live Site:** [webstaranalytics.com](https://www.webstaranalytics.com/)
## About

WebStar Analytics is an automated sports data science and pipeline platform that models and ranks all 365 NCAA Men's Division I College Basketball teams using adjusted
offensive and defensive efficiencies every day. These effencies are calculated by using a team's points per possesion scored and allowed, adjusting it based on opponent quality and home court advantage using a Bayesian hierarchical model. With these values, spreads and win probabilities are then calculated for that day's matchups, allowing the user to compare WebStar's results to other sportsbooks in order to make an educated decision. This project integrates AWS S3, EC2, CloudFront, and Python to efficiently manage data and deliver real-time predictions.

<!-- First image, width reduced to 400px -->
<img src="https://github.com/user-attachments/assets/a3b75fc8-af8a-45a8-a4d0-6ceb4a39dbb7" width="300" />

<!-- Second image, width reduced to 500px -->
<img src="https://github.com/user-attachments/assets/47f7b754-e8fc-404a-b870-f2c615cf6f9c" width="400" />

## Features

- Light weight website that displays up-to-date rankings for all 365 NCAA Men's College Basketball teams, sortable by offensive and defensive scores.
- Displays today's matchups along with the imputed spreads and win probabilities.
- Automated data pipeline using AWS EC2, while storing data and hosting website on AWS S3.
- Archives previous results which can be used to validate model accuracy on final scores.

## Technologies

- Python (pandas, numpy, boto3)
- AWS S3, EC2 (Ubuntu), CloudFront, EventBridge, shell scripting
- Git & GitHub for version control

## Architecture
- Every morning at 8 AM, AWS EventBridge calls on the dedicated AWS EC2 instance to wake up and automatically initialize the `main.py` script.
- In doing so, it first calls on `archive_game_results.py` to take yesterday's games, find the final scores, and store it on a dedicated file in the AWS S3. This file is used for analytics and to prevent the client having to load an entire season's worth of results, only for it to be filtered client side to display today's games.
- Next, `scrape_data.py` is ran, this computes all of yesterday's boxscores and computes neccessary variables such as points per possesion. These results are concatenated on the master.csv stored in AWS S3.
- Then, `execute_mcmc.py` is executed, this is where the model is reran with the most up to date numbers. This produces the current rankings for today.
- Lastly, `scrape_todays_games.py` is called to find today's games, and calculate their respective point spreads and win probabilities.
- Cache is then refreshed and then the EC2 instance is automatically switched off to save on resources.

## Future Work

- Integrate an up-to-date API onto various sportsbooks to determine which games have the largest edges to bet on

## Author

Ryan Webster

## License

This project is licensed under the MIT License.
