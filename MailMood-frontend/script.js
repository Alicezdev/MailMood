document.addEventListener('DOMContentLoaded', () => {
 
    const analyzeEmailsButton = document.getElementById('analyze-emails');

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
            
            console.log(`response json: ${data}`); // This will log the array of analyzed emails 

            const sliderContainer = $('#emailResponseSlider');


            // Clear previous slider content
            sliderContainer.html('');
            console.log(`sliderContainer is null?: ${sliderContainer.html}`); // Check if this is null
            // Iterate through each analyzed email
            data.forEach((email, index) => {
                const { subject, body, tone, mood_percentages, emoji } = email;
                
                console.log(`Email ${index + 1}:`);
                console.log(`tone: ${tone}`);
                console.log(`mood_percentages: ${mood_percentages}`);
                console.log(`emoji: ${emoji}`);
                
                let mood_percentages_list = [mood_percentages.neg, mood_percentages.neu, mood_percentages.pos];

                // Create a new slide item
                const slideItem = $(`
                <div class="slide-item">
                    <div><strong>Mood:</strong> ${tone} ${emoji}</div>
                    <div id="chartContainer${index + 1}" class="chart-container"></div>
                    <div><strong>Subject:</strong> ${subject}</div>
                    <div><strong>Body:</strong> ${body}</div>                                    
                </div>
                `);
                console.log(`slideItem: ${slideItem}`);
                console.log('Starting to append slides');
                sliderContainer.append(slideItem);
                console.log('Slide appended');

                // Example: Using the data to draw a pie chart for each email
                drawPieChart(mood_percentages_list, `chartContainer${index + 1}`);
            });
            // Initialize the Slick slider after appending the slides
            console.log(`sliderContainer.length: ${sliderContainer.length}`);
            if (sliderContainer.length > 0) {
                console.log('Initializing slider...');
                sliderContainer.slick({
                    infinite: true,
                    slidesToShow: 1,
                    slidesToScroll: 1,
                    dots: true,
                    arrows: true,
                });
                console.log('Slider initialized.');
            } else {
                console.error('Slider container not found');
            }
            console.log(`sliderContainer.length after initialize: ${sliderContainer.length}`);
        } catch (error) {
            console.error('Error:', error);
        }
    });
    
});

function drawPieChart(percentages, containerId)  {

    // Create a new canvas element for each chart
    const container = document.getElementById(containerId);
    console.log(`start to draw pie chart for container: ${container}`);
    // Clear any existing content in the container
    container.innerHTML = '';  
    // Create a new canvas element and append it to the container
    const canvas = document.createElement('canvas');
    container.appendChild(canvas);

    // Get the context for the newly created canvas
    const emotionPieChart = canvas.getContext('2d');
    new Chart(emotionPieChart, {
        type: 'pie',
        data: {
            labels: ['Negative', 'Neutral', 'Positive'],  // Adjust labels as needed
            datasets: [{
                data: percentages,
                backgroundColor: ['#EE7785', '#C89EC4', '#84B1ED']  // Adjust colors as needed
            }]
        },
        options: {
            responsive: false,  // Ensure it doesn't resize automatically
            maintainAspectRatio: false  // Allow the aspect ratio to be ignored
        }
    });
}

$(document).ready(function(){
    $('.one-time').slick({
      dots: true,
      infinite: true,
      speed: 300,
      slidesToShow: 1,
      adaptiveHeight: false
    });
  
    // Adjust height on resize
    $(window).resize(function(){
      adjustSliderHeight();
    });
  
    function adjustSliderHeight() {
      var $slickTrack = $('.one-time .slick-track');
      var slideHeight = $slickTrack.find('.slick-slide').outerHeight();
      $('.one-time').height(slideHeight);
    }
  
    // Adjust height initially
    adjustSliderHeight();
  });


