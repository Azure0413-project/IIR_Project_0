const timer1 = 0;
const timer2 = 0;
let recordId = null;
let feedback_btn = 1;

// enter button
document.getElementById('findRecipes').addEventListener('click', function() {
    this.disabled = true; // Disable the button to prevent further clicks

    // prompt
    const user_prompt = document.getElementById('foodPrompt').value;    
    if (user_prompt.trim() === "") {
        alert("Please enter a food preference or description.");
        return;
    } else {
        // Show waiting message with typing effect
        const waitingMessage = document.getElementById('waiting-message');
        waitingMessage.classList.remove('hidden');
        const text = "Please wait for the model analysis...";
        typeEffect(waitingMessage, text);

        // redirect after 3s
        setTimeout(() => { document.getElementById('query').classList.add('hidden'); }, timer1);

        //  user_id form html <script> 
        data = initialPost(user_id, user_prompt)
            .then(recordId => {
                console.log('Record ID:', recordId);
                waitingMessage.classList.add('hidden'); // Hide waiting message
            });
    }
});

// review
document.getElementById('goodButton').addEventListener('click', function() {
    feedback_btn = 1; 
    showAlert('Thanks for your review!');
    updateRecord(recordId, feedback_btn, null);
    location.reload();
});

document.getElementById('badButton').addEventListener('click', function() {
    feedback_btn = 0;
    document.getElementById('feedbackForm').classList.remove('hidden');
});

document.getElementById('submitFeedback').addEventListener('click', function() {
    const feedback = document.getElementById('feedbackText').value;
    if (feedback.trim() === "") {
        alert("Please enter your feedback before submitting.");
        return;
    }
    updateRecord(recordId, feedback_btn, feedback);
    console.log('record id:', recordId);
    console.log('feedback_btn:', feedback_btn);
    console.log('feedback:', feedback);
    console.log('done feedback');

    showAlert('Thank you for your feedback!');
    document.getElementById('feedbackForm').classList.add('hidden');
    document.getElementById('feedbackText').value = ''; // Clear feedback field
    location.reload();
});

function showAlert() {
    alert('Thanks for your review!');
    location.reload();
}

// api get
async function initialPost(user, prompt) {
    console.log('user:', user);
    console.log('prompt:', prompt);

    try {
        const response = await fetch('api/get_data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user, prompt }),
        });
        
        if (response.ok) {
            console.log('initial post response ok');
            const data = await response.json();
            console.log(data);
            recordId = data.record_id;
            console.log('record id:', recordId);
            show(data, prompt);             
            return data;

        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function updateRecord(recordId, responseAgree, feedback) {
    try {
        const response = await fetch('api/store_data/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ record_id: recordId, response_agree: responseAgree, feedback: feedback }),
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Update record response ok:', data);
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

// show results
function show(data, prompt) {
    // // nonsense response
    // const stringContainer = document.getElementById('nonsense-response');
    // const text = "Thanks for your patience! I’m just putting together the information you need. This may take a few moments, I appreciate your understanding and will have the information for you shortly.";
    // setTimeout(() => { typeEffect(stringContainer, text); }, timer1 + 1000);
    // setTimeout(() => { document.getElementById('nonsense-response').classList.add('hidden'); }, timer1 + timer2);

    // rag response
    const stringContainer2 = document.getElementById('rag-response');
    setTimeout(() => { stringContainer2.innerText = data.new_prompt; }, timer1 + timer2);

    // make data into foodInfo
    const foodInfo = [
        {
            vendor: data.restaurant_name[0],
            product_name: data.food_name[0],
            product_price: data.food_price[0],
            product_img: data.image_url_1,
            map: data.google_map[0]
        },
        {
            vendor: data.restaurant_name[1],
            product_name: data.food_name[1],
            product_price: data.food_price[1],
            product_img: data.image_url_2,
            map: data.google_map[1]
        },
        {
            vendor: data.restaurant_name[2],
            product_name: data.food_name[2],
            product_price: data.food_price[2],
            product_img: data.image_url_3,
            map: data.google_map[2]
        },
    ];

    // Display recipes
    const recommendationList = document.getElementById('recommendationList'); // Ensure this element exists
    foodInfo.forEach(recipe => {
        const listItem = document.createElement('li');
        listItem.className = 'recipe-card';
        listItem.innerHTML = `
            <img src="${recipe.product_img}" alt="${recipe.vendor}">
            <h3>${recipe.product_name}</h3>
            <p>Restaurant: ${recipe.vendor}</p>
            
            <p>Price: ${recipe.product_price} NTD</p>
            <a href=${recipe.map}>Shows on map</a>
          
        `;
        recommendationList.appendChild(listItem);
    });

    // Show results section delay=10s
    setTimeout(() => {
        document.getElementById('recommendation').classList.remove('hidden');
    }, timer1 + timer2);
}

// typing effect
function typeEffect(element, text, delay = 150) {
    let index = 0;
    function typeNextCharacter() {
        if (index < text.length) {
            element.innerHTML += text[index];
            index++;
            setTimeout(typeNextCharacter, delay); // Delay before the next character appears
        }
    }
    typeNextCharacter(); // Start the typing effect
}