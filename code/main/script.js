

document.getElementById('findRecipes').addEventListener('click', function() {



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
    document.getElementById('foodPrompt').value = '';


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
   const recipes = [
    {
        title: "Beef Burger",
        image: "https://cdn2.tmbi.com/TOH/Images/Photos/37/1200x1200/exps41063_SD163614D12_01_3b.jpg",
        description: "Consists of a seasoned ground beef patty cooked to your desired level of doneness, usually served in a toasted bun. ",
        tags: ["beef", "chicken"]
    },
    {
        title: "Beef Noodle Soup",
        image: "https://th.bing.com/th/id/OIP.0oNApt7arC9WlQN6vLotJQHaHa?rs=1&pid=ImgDetMain",
        description: "A refreshing noodle soup with beef.",
        tags: ["beef", "noodle"]
    },
    {
        title: "Beef Steak",
        image: "https://th.bing.com/th/id/OIP.5g8-3tuYrdHuJn2-iYVzGwAAAA?rs=1&pid=ImgDetMain",
        description: "A beef steak is a flavorful and tender cut of beef, typically grilled or pan-seared to perfection.",
        tags: ["beef", "stir-fry"]
    },
];

    // Filter recipes based on the prompt
    const filteredRecipes = recipes.filter(recipe => 
        recipe.tags.some(tag => prompt.includes(tag))
    );
    console.log(filteredRecipes)

    // If no recipes match, show a default message
    if (filteredRecipes.length === 0) {
        filteredRecipes.push({
            title: "No Recommendations",
            image: "https://via.placeholder.com/150",
            description: "Sorry, we couldn't find any recommendations for your prompt."
        });
    }

    // Clear previous results
    const recommendationList = document.getElementById('recommendationList');
    recommendationList.innerHTML = '';

    // Display recipes
    filteredRecipes.forEach(recipe => {
        const listItem = document.createElement('li');
        listItem.className = 'recipe-card';
        listItem.innerHTML = `
            <img src="${recipe.image}" alt="${recipe.title}">
            <h3>${recipe.title}</h3>
            <p>${recipe.description}</p>
        `;
        recommendationList.appendChild(listItem);
    });

    // Show results section
    document.getElementById('recommendations').classList.remove('hidden');
});

