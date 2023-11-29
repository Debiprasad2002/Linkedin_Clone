function search() {
    var query = document.getElementById("query").value;

    // Send the query to the backend
    fetch('http://127.0.0.1:5000/search', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: query }),
    })
    .then(response => response.json())
    .then(data => {
        displayResults(data.results);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayResults(results) {
    var resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "";

    if (results.length === 0) {
        resultsDiv.innerHTML = "<p>No results found.</p>";
        return;
    }

    resultsDiv.innerHTML = "<h2>Search Results:</h2>";
    results.forEach(result => {
        resultsDiv.innerHTML += `<p>${result.name} - ${result.job_preferences || result.profile}</p>`;
    });
}


// Existing script.js code remains unchanged

function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const chatContainer = document.getElementById('chat-container');

    const messageContent = messageInput.value.trim();

    if (messageContent !== '') {
        const newMessage = document.createElement('div');
        newMessage.classList.add('message');
        newMessage.textContent = messageContent;

        chatContainer.appendChild(newMessage);

        // Clear the message input
        messageInput.value = '';

        // Optionally, you can handle sending the message to a server or perform other actions.
        // For simplicity, this example only updates the UI.
    }
}



