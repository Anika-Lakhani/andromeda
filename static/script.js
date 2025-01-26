document.addEventListener('DOMContentLoaded', function() {
    // Load initial content
    loadContent('company');

    // Add tab click handlers
    document.querySelectorAll('.tab-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const tab = this.getAttribute('href').substring(1);
            document.querySelectorAll('.tab-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            loadContent(tab);
        });
    });
});

async function loadContent(tab) {
    const contentDiv = document.getElementById('content');
    
    switch(tab) {
        case 'company':
            const companyResponse = await fetch('/company_overview');
            contentDiv.innerHTML = await companyResponse.text();
            break;
        case 'responsibilities':
            const respResponse = await fetch('/intern_responsibilities');
            contentDiv.innerHTML = await respResponse.text();
            break;
        case 'tools':
            const toolsResponse = await fetch('/tools_technologies');
            contentDiv.innerHTML = await toolsResponse.text();
            break;
        case 'expectations':
            const expResponse = await fetch('/project_expectations');
            contentDiv.innerHTML = await expResponse.text();
            break;
        case 'save':
            const saveResponse = await fetch('/save_conversation', { method: 'POST' });
            const result = await saveResponse.json();
            contentDiv.innerHTML = `<p>${result.result}</p>`;
            break;
    }
}

async function askQuestion(section) {
    console.log(`Asking question for section: ${section}`);
    const question = document.getElementById(`${section}-question`).value;
    console.log(`Question: ${question}`);
    
    try {
        const response = await fetch(`/${section}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        console.log('Response received:', data);
        
        const responseElement = document.getElementById(`${section}-response`);
        if (responseElement) {
            responseElement.innerHTML = data.response;
            responseElement.style.display = 'block'; // Make sure it's visible
        } else {
            console.error(`Response element not found for section: ${section}`);
        }
    } catch (error) {
        console.error('Error asking question:', error);
    }
}

async function selectInternType(section) {
    console.log(`Selecting intern type for section: ${section}`);
    const internType = document.getElementById(`${section}-intern-type`).value;
    console.log(`Selected type: ${internType}`);
    
    if (!internType) return; // Don't proceed if no type selected
    
    try {
        const response = await fetch(`/${section}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ intern_type: internType })
        });
        
        const data = await response.json();
        console.log('Response received:', data);
        
        const contentElement = document.getElementById(`${section}-content`);
        if (contentElement && data.responsibilities) {
            contentElement.innerHTML = data.responsibilities;
            contentElement.style.display = 'block';
        } else {
            console.error(`Content element not found or no responsibilities in response`);
        }
    } catch (error) {
        console.error('Error selecting intern type:', error);
    }
} 