import React from 'react';
import './App.css';
import Form from './Form.js';

class App extends React.Component {
    render () {
        return (
            <div className="main">
                <Form test="Essa" />
                <Form test="Essa 2" />
            </div>
        )
    }
}

export default App;