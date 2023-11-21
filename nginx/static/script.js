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
        console.log('ScannerId:', scanner_id);
        console.log('ConfigId:', config_id);

    } catch (error) {
        console.error('Error:', error);
    }
}
