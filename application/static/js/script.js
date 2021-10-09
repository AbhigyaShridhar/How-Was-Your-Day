// console.log("JS Connected");

// Function for Validating Registration Form
function validateRegsitrationForm() {
    
    // Grabbing the Form Fields
    var name = document.forms["registrationForm"]["name"].value;
    var email = document.forms["registrationForm"]["email"].value;
    var password = document.forms["registrationForm"]["password"].value;

    // Checking if name, email and password are empty when user hits Register Button
    if(name == "" || name == null || email == "" || email == null || password == "" || password == null) {
        alert("Please Fill the below Details !!!");
        return false;
    } else {
        alert("Your Details Submitted... You are now Registered with 'How was your Day 🤔'");
        return true;
    }
}


// Function for Validating Login Form
function validateLoginForm() {

    // Grabbing the Form Fields
    var email = document.forms["loginForm"]["email"].value;
    var password = document.forms["loginForm"]["password"].value;

    // Checking if email and password are empty when user hits Login Button
    // Login the User if its demo@gmail and password = 12345
    // Else throw error
    if(email == "" || email == null || password == "" || password == null) {
        alert("Please Fill the below Details !!!");
        return false;
    } else if(email == "demo@gmail.com" && password == "12345") {
        alert("Welcome Demo");
        alert("Logged In Successfully 😃");
        return true;
    } else {
        alert("Invalid Credentials");
        return true;
    }
}