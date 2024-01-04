"use client"
import { useState } from 'react';

const LoginForm = () => {
    const [email, setEmail] = useState('tony@montana.com');
    const [password, setPassword] = useState('ComplexPass1234');
    const [success, setSuccess] = useState(false)

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            const response = await fetch('http://localhost:8080/api/v1/auth/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    email,
                    password,
                }),
                credentials: 'include', // This is equivalent to withCredentials: true in Axios
            });

            // Handle the response
            if (response.ok) {
                const data = await response.json();
                console.log('Login success:', data);
                setSuccess(true)
                alert("Login Success")

            } else {
                setSuccess(false)
                // Handle login failure
                console.error('Login failed:', response.status);
            }
        } catch (error) {
            // Handle specific error cases or provide a generic error message
            console.error('Error during login:', error);
        }
    };

    return (
        <>
            <h1 className='w-full text-center mt-5 text-3xl '>Login</h1>
            <form onSubmit={handleSubmit} className="max-w-md mx-auto my-4 p-6 bg-white shadow-md rounded-md">
                <label className="block mb-2">
                    <span className="text-gray-700">Email:</span>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        className="w-full mt-1 p-2 border rounded-md focus:outline-none focus:border-blue-500 text-black"
                    />
                </label>
                <br />
                <label className="block mb-2">
                    <span className="text-gray-700">Password:</span>
                    <input
                        type=""
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        className="w-full mt-1 p-2 border rounded-md focus:outline-none focus:border-blue-500 text-black"
                    />
                </label>
                <br />
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white p-2 rounded-md hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue"
                >
                    Login
                </button>
            </form>
            <div className={`${success ? 'bg-green-400' : 'bg-gray-700'} w-full text-center h-20`}>
                Success?
            </div>
        </>


    );
};

export default LoginForm;