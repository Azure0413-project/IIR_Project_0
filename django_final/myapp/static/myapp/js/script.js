

const timer1 = 0;
const timer2 = 0;
let recordId = null ;


// enter button
document.getElementById('findRecipes').addEventListener('click', function() {

    this.disabled = true; // Disable the button to prevent further clicks

    // prompt
    const user_prompt = document.getElementById('foodPrompt').value;    
    if (user_prompt.trim() === "") {
        alert("Please enter a food preference or description.");
        return;
    }
    else {
        // redirect after 3s
        setTimeout(() => { document.getElementById('query').classList.add('hidden');},timer1);

    }


    //  user_id form html <script> 
    
    data = initialPost(user_id, user_prompt)
        .then(recordId => {
            console.log('Record ID:', recordId);
        });

});


// review
document.getElementById('goodButton').addEventListener('click', function() {
    showAlert('Thanks for your review!');
});

document.getElementById('badButton').addEventListener('click', function() {
    document.getElementById('feedbackForm').classList.remove('hidden');
});

document.getElementById('submitFeedback').addEventListener('click', function() {

    const feedback = document.getElementById('feedbackText').value;
    if (feedback.trim() === "") {
        alert("Please enter your feedback before submitting.");
        return;
    }
    updateRecord(recordId, true, feedback);
    console.log('record id:',recordId);
    console.log('feedback:',feedback);
    console.log('done feedback');

    showAlert('Thank you for your feedback!');
    document.getElementById('feedbackForm').classList.add('hidden');
    document.getElementById('feedbackText').value = ''; // Clear feedback field



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
            console.log('initial post response ok')
            const data = await response.json();
            console.log(data);
            // html
            recordId = data.record_id;
            console.log('record id:',recordId);
            show(data,prompt);             
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
function show(data,prompt){

    // nonsense response
    const stringContainer = document.getElementById('nonsense-response');
    const text = "Thanks for your patience! I’m just putting together the information you need. This may take a few moments, I appreciate your understanding and will have the information for you shortly."
    setTimeout(() => { typeEffect(stringContainer, text);}, timer1 + 1000);
    setTimeout(() => { document.getElementById('nonsense-response').classList.add('hidden');},timer1+timer2);


    // rag response
    const stringContainer2 = document.getElementById('rag-response');
    setTimeout(() => { stringContainer2.innerText = data.new_prompt}, timer1 + timer2);

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
     foodInfo.forEach(recipe => {
         const listItem = document.createElement('li');
         listItem.className = 'recipe-card';
         listItem.innerHTML = `
             <img src="${recipe.product_img}" alt="${recipe.vendor}">
             <h3>${recipe.product_name}</h3>
             <p>Restaurant: ${recipe.vendor}</p>
             <p>Price: ${recipe.product_price} NTD</p>
             <p>
                <span style="font-size: 0.65rem;">Location:</span><br>
                <span style="font-size: 0.55rem;">${recipe.map}</span>
            </p>
         `;
         recommendationList.appendChild(listItem);
     });
 



     // Show results section delay=10s
     setTimeout(() => {
        document.getElementById('recommendation').classList.remove('hidden');
    }, timer1 + timer2 );


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
