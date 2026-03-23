// script.js

document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.getElementById('login-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const welcome = document.getElementById('welcome');
    const loginForm = document.getElementById('login-form');
    const submitLogin = document.getElementById('submit-login');
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    
    const changeAddressBtn = document.getElementById('change-address-btn');
    const addressForm = document.getElementById('address-form');
    const newAddressInput = document.getElementById('new-address');
    const submitAddress = document.getElementById('submit-address');
    const addressDisplay = document.getElementById('address-display');
  
    // Show login form when login button is clicked
    loginBtn.addEventListener('click', () => {
      loginForm.style.display = 'block';
    });
  
    // Handle login form submission
    submitLogin.addEventListener('click', async () => {
      const username = usernameInput.value;
      const password = passwordInput.value;
      try {
        const response = await fetch('/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        const result = await response.json();
        if (result.success) {
          welcome.textContent = 'Hello, ' + result.user;
          loginBtn.style.display = 'none';
          logoutBtn.style.display = 'inline-block';
          loginForm.style.display = 'none';
          addressDisplay.textContent = result.address || addressDisplay.textContent;
        } else {
          alert('Login failed');
        }
      } catch (error) {
        console.error('Error during login:', error);
      }
    });
  
    // Handle logout
    logoutBtn.addEventListener('click', async () => {
      try {
        await fetch('/logout');
        welcome.textContent = 'Not logged in';
        loginBtn.style.display = 'inline-block';
        logoutBtn.style.display = 'none';
      } catch (error) {
        console.error('Error during logout:', error);
      }
    });
  
    // Show address form when button clicked
    changeAddressBtn.addEventListener('click', () => {
      addressForm.style.display = 'block';
    });
  
    // Handle address update submission
    submitAddress.addEventListener('click', async () => {
      const newAddress = newAddressInput.value;
      try {
        const response = await fetch('/update_address', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ address: newAddress })
        });
        const result = await response.json();
        if (result.success) {
          addressDisplay.textContent = result.address;
          addressForm.style.display = 'none';
        } else {
          alert('Update failed');
        }
      } catch (error) {
        console.error('Error updating address:', error);
      }
    });
  
    // Check login status on load
    (async () => {
      try {
        const response = await fetch('/user');
        const result = await response.json();
        if (result.user) {
          welcome.textContent = 'Hello, ' + result.user;
          loginBtn.style.display = 'none';
          logoutBtn.style.display = 'inline-block';
          addressDisplay.textContent = result.address || addressDisplay.textContent;
        }
      } catch (error) {
        console.error('Error fetching user status:', error);
      }
    })();
  
  });
  