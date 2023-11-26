async function get_version() {
	const res = fetch("/api/version")
		.then((res) => res.json())
		.then((json) =>	{
			console.log(json);
		});
}

async function get_scanners() {
	const res = fetch("/api/scanners")
		.then((res) => res.json())
		.then((json) =>	{
			console.log(json);
		});
}

async function get_configs() {
	const res = fetch("/api/configs")
		.then((res) => res.json())
		.then((json) =>	{
			console.log(json);
		});
}

async function createTarget() {
    const form = document.getElementById('createTargetForm');
    const formData = new FormData(form);

    const requestBody = {};
    for (const [key, value] of formData.entries()) {
        requestBody[key] = value;
    }

    try {
        const response = await fetch('/api/targets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();
        console.log('Target created with UUID:', data.UUID);
        // Handle the response data as needed
    } catch (error) {
        console.error('Error:', error);
    }
}

async function createTask() {
    const taskName = document.getElementById('taskName').value;
    const configId = document.getElementById('configId').value;
    const scannerId = document.getElementById('scannerId').value;
    const targetId = document.getElementById('targetId').value;

    const requestBody = {
        name: taskName,
        config_id: configId,
        scanner_id: scannerId,
        target_id: targetId
    };

    try {
        const response = await fetch('/api/create_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();
        console.log('Task created with UUID:', data.UUID);

    } catch (error) {
        console.error('Error:', error);
    }
}

async function startTask() {
    const taskId = document.getElementById('taskId').value;

    const requestBody = {
        task_id: taskId
    };

    try {
        const response = await fetch('/api/start_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });

        const data = await response.json();
        console.log('Task Status:', data.status);

    } catch (error) {
        console.error('Error:', error);
    }
}

async function checkTaskProgress() {
    const taskId = document.getElementById('taskId').value;

    try {
        console.log('Task ID:', taskId);
        const response = await fetch(`/api/task_progress/${taskId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        console.log('Response Status:', response.status);
        console.log('Response Headers:', response.headers);
        
        const data = await response.json();
        const progressOutput = document.getElementById('progressOutput');

        if (response.ok) {
            console.log('Received Data:', data);
	    console.log('Progress:', progressOutput);
            progressOutput.innerHTML = `
                <p>Status: ${data.status}</p>
                <p>Progress: ${data.progress}</p>
            `;
        } else {
            progressOutput.innerHTML = `<p>Error: Unable to fetch task progress</p>`;
        }
    } catch (error) {
        console.error('Error:', error);
    }
}

async function fetchReportProgress() {
    const reportId = document.getElementById('reportId').value;

    try {
        const response = await fetch(`/api/report_progress/${reportId}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const data = await response.json();
            return data.progress;
        } else {
            console.error('Failed to fetch report progress');
            return null;
        }
    } catch (error) {
        console.error('Error fetching report progress:', error);
        return null;
    }
}

async function getReportProgress() {
    const reportId = document.getElementById('reportId').value;

    if (!reportId) {
        console.error('Please enter a Report ID');
        return;
    }

    const progress = await fetchReportProgress(reportId);

    if (progress !== null) {
        console.log(`Report Progress for ID ${reportId}: ${progress}`);
    } else {
        console.error('Failed to fetch report progress');
    }
}

async function getReport() {
  const reportId = document.getElementById('reportId').value;

  try {
    const response = await fetch(`/api/report/${reportId}.pdf`, {
      method: 'GET',
    });

    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      
      // Open the PDF in a new tab
      window.open(url, '_blank');
    } else {
      console.error('Failed to retrieve the report');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}

