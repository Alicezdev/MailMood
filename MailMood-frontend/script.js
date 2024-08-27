document.addEventListener('DOMContentLoaded', () => {
    const emailForm = document.getElementById('email-form');
    const loadEmailsButton = document.getElementById('load-emails');
    const emailListDiv = document.getElementById('email-list');
    const parseEmailsButton = document.getElementById('parse-emails');
    const analyzeEmailsButton = document.getElementById('analyze-emails');


    // analyzeEmailsButton.addEventListener('click', async (e) => {
    //     e.preventDefault();
    //     const target_email = document.getElementById('target_email').value;
    //     /* const response =  */await fetch('http://127.0.0.1:3000/analyze-email', {
    //         method: 'POST',
    //         headers: {
    //             'Content-Type': 'application/json'
    //         },
    //         body: JSON.stringify({target_email})
    //     })
    //     .then(response => response.json())
    //     .then(data => {
    //         console.log(data); 
    //         const tone = data.tone;
    //         const mood_percentages = data.mood_percentages;
    //         const emoji = data.emoji;
    
      
    //         // You can now use these values in your frontend
    //         console.log(tone); 
    //         console.log(mood_percentages); 
    //         console.log(emoji); 
    //         let mood_percentages_list = [mood_percentages.neg, mood_percentages.neu, mood_percentages.pos];

  
      
    //         // Example: Using the data to draw a pie chart
    //         drawPieChart(mood_percentages_list);
    //     });

    //     const email = await response.json();
    //     console.log(email)
    //     const subjectResponse = document.getElementById('responseSubject');
    //     const bodyResponse = document.getElementById('responseBody');
    //     const analyzeResponse = document.getElementById('response');
        
    //     console.log(analyzeResponse)
    //     analyzeResponse.innerHTML = `Tone: ${email.tone}`;
    //     subjectResponse.innerHTML = `Subject: ${email.subject}`;
    //     bodyResponse.innerHTML = `Body: ${email.body}`;
    // });

    analyzeEmailsButton.addEventListener('click', async (e) => {
        e.preventDefault();
        
        const target_email = document.getElementById('target_email').value;
    
        try {
            const response = await fetch('http://127.0.0.1:3000/analyze-email', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ target_email })
            });
            
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const data = await response.json();
            
            console.log(data);
            
            const { tone, mood_percentages, emoji } = data;
            
            console.log(tone);
            console.log(mood_percentages);
            console.log(emoji);
            
            let mood_percentages_list = [mood_percentages.neg, mood_percentages.neu, mood_percentages.pos];
            
            // Example: Using the data to draw a pie chart
            drawPieChart(mood_percentages_list);
    
            const subjectResponse = document.getElementById('responseSubject');
            const bodyResponse = document.getElementById('responseBody');
            const analyzeResponse = document.getElementById('response');

            analyzeResponse.innerHTML = `Tone: ${tone}${emoji}`;
            subjectResponse.innerHTML = `Subject: ${data.subject}`;
            bodyResponse.innerHTML = `Body: ${data.body}`;
        } catch (error) {
            console.error('Error:', error);
        }
    });
    

});

function drawPieChart(percentages) {
    const emotionPieChart = document.getElementById('emotionPieChart').getContext('2d');
    new Chart(emotionPieChart, {
        type: 'pie',
        data: {
            labels: ['Negative', 'Neutral', 'Positive'],  // Adjust labels as needed
            datasets: [{
                data: percentages,
                backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56']  // Adjust colors as needed
            }]
        },
        options: {
            responsive: false,  // Ensure it doesn't resize automatically
            maintainAspectRatio: false  // Allow the aspect ratio to be ignored
        }
    });
}
