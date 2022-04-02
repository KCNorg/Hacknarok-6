import React from "react";
import "./App.css";
import InputForm from "./InputForm.js";

class App extends React.Component {
    render() {
        return (
            <div className="container py-3">
            <header>
                <div className="d-flex flex-column flex-md-row align-items-center pb-3 mb-4 border-bottom">
                <a href="/" className="d-flex align-items-center text-dark text-decoration-none">
                    <span className="fs-4">Pricing example</span>
                </a>

                <nav className="d-inline-flex mt-2 mt-md-0 ms-md-auto">
                    <a className="me-3 py-2 text-dark text-decoration-none" href="#">Features</a>
                    <a className="me-3 py-2 text-dark text-decoration-none" href="#">Enterprise</a>
                    <a className="me-3 py-2 text-dark text-decoration-none" href="#">Support</a>
                    <a className="py-2 text-dark text-decoration-none" href="#">Pricing</a>
                </nav>
                </div>

                <div className="pricing-header p-3 pb-md-4 mx-auto text-center">
                <h1 className="display-4 fw-normal">Pricing</h1>
                <p className="fs-5 text-muted">Quickly build an effective pricing table for your potential customers with this Bootstrap example. Is built with default Bootstrap components and utilities with little customization.</p>
                </div>
            </header>

            <main>
                {/* <div className="row row-cols-1 row-cols-md-3 mb-3 text-center"> */}
                <div class="container">
                <div class="row justify-content-md-center">
                    <div class="col col-lg-6">
                        <div className="form-wrapper">
                            <h4>Contact Us</h4>
                            <InputForm id="InputForm"/>
                        </div>
                    </div>
                </div>
                {/* <div class="row">
                    <div class="col">
                    1 of 3
                    </div>
                    <div class="col-md-auto">
                    Variable width content
                    </div>
                    <div class="col col-lg-2">
                    3 of 3
                    </div>
                </div> */}
                </div>
            </main>

            <footer className="pt-4 my-md-5 pt-md-5 border-top">
                <div className="row">
                    <div className="col-12 col-md">
                        <small className="d-block mb-3 text-muted">&copy; 2017–2021</small>
                    </div>
                    <div className="col-6 col-md">
                        <h5>Features</h5>
                    </div>
                    <div className="col-6 col-md">
                        <h5>Resources</h5>
                    </div>
                    <div className="col-6 col-md">
                        <h5>About</h5>
                    </div>
                </div>
            </footer>
            </div>
        )
    }
}

export default App;
