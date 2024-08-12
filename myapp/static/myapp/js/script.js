

document.getElementById('findRecipes').addEventListener('click', function() {

    // Read CSV
    const shop_csv = [  "2000,九州豚骨拉麵 (台南南門店),豚骨拉麵, 120,https://images.deliveryhero.io/image/fd-tw/Products/2047873.jpg?width=150&height=150",
                         "2001,九州豚骨拉麵 (台南南門店),地獄拉麵, 130,https://images.deliveryhero.io/image/fd-tw/Products/2047878.jpg?width=150&height=150",
                         "2002,九州豚骨拉麵 (台南南門店),味噌拉麵, 130,https://images.deliveryhero.io/image/fd-tw/Products/2047877.jpg?width=150&height=150"
                    ]; 
                
    // Convert shop_list to an array of objects
    const shop_dict = shop_csv.map(item => {
        const [id, vendor, product_name, product_price, product_img] = item.split(',');
        return {
            id: id.trim(),
            vendor: vendor.trim(),
            product_name: product_name.trim(),
            product_price: product_price.trim(),
            product_img: product_img.trim()
        };
    });

    console.log(shop_dict); 

    // prompt
    const prompt = document.getElementById('foodPrompt').value;    
    if (prompt.trim() === "") {
        alert("Please enter a food preference or description.");
        return;
    }
    else {
        document.getElementById('query').classList.add('hidden');
    }

    // Clear the input field
    // document.getElementById('foodPrompt').value = '';


    // review part
    document.getElementById('goodButton').addEventListener('click', function() {
        showAlert();
    });
    
    document.getElementById('badButton').addEventListener('click', function() {
        showAlert();
    });
    
    function showAlert() {
        alert('Thanks for your review!');
        location.reload();
    }


   // Sample recipe data with tags
   const foodInfo = [
    {
        vendor: shop_dict[0]['vendor'],
        product_name: shop_dict[0]['product_name'],
        product_price: shop_dict[0]['product_price'],
        product_img: shop_dict[0]['product_img'],
        tags: ["ramen"]
    },
    {
        vendor: shop_dict[1]['vendor'],
        product_name: shop_dict[1]['product_name'],
        product_price: shop_dict[1]['product_price'],
        product_img: shop_dict[1]['product_img'],
        tags: ["ramen"]
    },
    {
        vendor: shop_dict[2]['vendor'],
        product_name: shop_dict[2]['product_name'],
        product_price: shop_dict[2]['product_price'],
        product_img: shop_dict[2]['product_img'],
        tags: ["ramen"]
    },
];

    // Filter recipes based on the prompt
    const filteredFood = foodInfo.filter(recipe => 
        recipe.tags.some(tag => prompt.includes(tag))
    );
    console.log(filteredFood)

    // If no recipes match, show a default message
    if (filteredFood.length === 0) {
        filteredFood.push({
            title: "No Recommendations",
            image: "https://via.placeholder.com/150",
            description: "Sorry, we couldn't find any recommendations for your prompt."
        });
    }

    // Clear previous results
    const recommendationList = document.getElementById('recommendationList');
    recommendationList.innerHTML = '';

    // Display recipes
    filteredFood.forEach(recipe => {
        const listItem = document.createElement('li');
        listItem.className = 'recipe-card';
        listItem.innerHTML = `
            <img src="${recipe.product_img}" alt="${recipe.vendor}">
            <h3>${recipe.product_name}</h3>
            <p>${recipe.vendor}</p>
            <p>Price: ${recipe.product_price} NTD</p>
        `;
        recommendationList.appendChild(listItem);
    });

    // Show results section
    document.getElementById('recommendation').classList.remove('hidden');
});

// api get
async function fetchData(user, prompt) {
    try {
        const response = await fetch('/api/endpoint/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user, prompt }),
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log(data);
        } else {
            console.error('Error:', response.statusText);
        }
    } catch (error) {
        console.error('Error:', error);
    }
}
fetchData('example_user', 'What do you want to eat today?');