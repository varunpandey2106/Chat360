document.addEventListener('DOMContentLoaded', () => {
 let formElement = document.getElementById('form');

    let handleSubmit = async (e) => {
        e.preventDefault()

        let friendVC = e.target.friendVC.value.toUpperCase()
        let name = e.target.name.value

        let response = await fetch('/get_token/?friendVC=' +friendVC);
        if (!response.ok) {
            // Handle non-successful responses here (e.g., display an error message).
            console.error("Error fetching data:", response.status, response.statusText);
            return true;
        }
        
        let data;
        try {
            data = await response.json();
        } catch (error) {
            console.error("Error parsing JSON response:", error);
            return true ;
        }
        


        let UID = data.uid
        let token = data.token

        sessionStorage.setItem('UID', UID)
        sessionStorage.setItem('token', token)
        sessionStorage.setItem('friendVC', friendVC)
        sessionStorage.setItem('name', name)

        window.open('/friendVC/', '_self')
    }
    formElement.addEventListener('submit', handleSubmit);
});

