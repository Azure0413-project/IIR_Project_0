

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
const formData = new FormData();
formData.append('user', user);
formData.append('prompt', prompt);

// 添加圖片 URL
formData.append('response_image_url_1', 'http://example.com/image1.jpg');
formData.append('response_image_url_2', 'http://example.com/image2.jpg');
formData.append('response_image_url_3', 'http://example.com/image3.jpg');

fetch('/api/post-data/', {
    method: 'POST',
    body: formData
})
.then(response => response.json())
.then(data => {
    if (data.status === 'Data received and saved successfully') {
        return fetch(`/api/get-data/?user=${user}`);
    } else {
        throw new Error('Error sending POST data');
    }
})
.then(response => response.json())
.then(data => {
    document.getElementById('query').innerHTML = `
        <h2>${data.new_prompt}</h2>
    `;

    recommendationList.innerHTML = '';

    data.response_text.forEach(text => {
        const li = document.createElement('li');
        li.textContent = text;
        recommendationList.appendChild(li);
    });

    data.response_image.forEach(image => {
        if (image) {
            const img = document.createElement('img');
            img.src = image; 
            img.alt = 'Recommendation Image';
            recommendationList.appendChild(img);
        }
    });

    recommendationSection.classList.remove('hidden'); 
})
.catch(error => console.error('Error:', error));