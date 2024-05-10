// Import necessary modules
const express = require('express');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Specify the absolute path to the SQLite database file
const DB_PATH = 'C:/Users/bhupe/myanimalvoting_app/votes.db';

const db = new sqlite3.Database(DB_PATH);

// Set the path to the views directory
app.set('views', path.join(__dirname, 'views'));

// Set the view engine to use EJS
app.set('view engine', 'ejs');

// Define route to handle requests for voting results
app.get('/results', (req, res) => {
    // Fetch voting results from the database
    db.get('SELECT SUM(count) as totalVotes FROM votes', (err, row) => {
        if (err) {
            console.error(err.message);
            res.status(500).send('Internal Server Error');
            return;
        }

        const totalVotes = row.totalVotes || 0;

        // Fetch votes for each option
        db.all('SELECT option, SUM(count) as votes FROM votes GROUP BY option', (err, rows) => {
            if (err) {
                console.error(err.message);
                res.status(500).send('Internal Server Error');
                return;
            }

            // Calculate percentages for each option
            const optionsWithPercentages = rows.map(row => {
                const percentage = ((row.votes / totalVotes) * 100).toFixed(2);
                return {
                    option: row.option,
                    votes: row.votes,
                    percentage
                };
            });

            // Render the results template with the voting results data
            res.render('results', {
                options: optionsWithPercentages // Pass optionsWithPercentages to the template
            });
        });
    });
});

// Start the server
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
