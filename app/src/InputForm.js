import React from 'react';
import { Formik, Field, Form } from 'formik';


const InputForm = (props) => {

    const validateForm = values => {
        const errors = {};
        if (!values.name) {
            errors.name = 'Name is required';
        } else if (values.name.length > 15) {
            errors.name = 'Must be 15 characters or less';
        }


        if (!values.email) {
            errors.email = 'Email is required';
        } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
            errors.email = 'Invalid email address';
        }


        if (!values.subject) {
            errors.subject = 'Subject is required';
        }

        return errors;
    };


    return (
        <Formik
            initialValues={{ name: '', email: '', subject: '', content: '' }}
            onSubmit={(values, { setSubmitting }) => {
                setTimeout(() => {

                    alert(JSON.stringify(values, null, 2));
                    setSubmitting(false);
                    props.handler(1);

                }, 1000);
            }}
            validate={validateForm}
        >
            {(formik, isSubmitting) => (
                <Form className="row g-3">                    
                    <div className="form-group">
                        <label htmlFor="name">Name</label>
                        <Field name="name" className={(formik.touched.name && formik.errors.name) ? 'form-control is-invalid' : 'form-control'} type="text" />
                        
                        {formik.touched.name && formik.errors.name ? (
                            <div className="invalid-feedback">{formik.errors.name}</div>
                        ) : null}
                    </div>

                    <div className="form-group">
                        <label htmlFor="email">Email Address</label>
                        <Field name="email" className={(formik.touched.email && formik.errors.email) ? 'form-control is-invalid' : 'form-control'} type="email" />
                        
                        {formik.touched.email && formik.errors.email ? (
                            <div className="invalid-feedback">{formik.errors.email}</div>
                        ) : null}
                    </div>

                    <div className="form-group">
                        <label htmlFor="subject">Subject</label>
                        <Field name="subject" className={(formik.touched.subject && formik.errors.subject) ? 'form-control is-invalid' : 'form-control'} type="text" />
                        
                        {formik.touched.subject && formik.errors.subject ? (
                            <div className="invalid-feedback">{formik.errors.subject}</div>
                        ) : null}
                    </div>

                    <div className="form-group">
                        <label htmlFor="content">Content</label>
                        <Field name="content" className="form-control" as="textarea" rows={3} cols={10} />
                    </div>

                    <div className="form-group">
                        <div className="row justify-content-center">
                            <div className="col col-lg-4">
                                <button type="submit" className="btn btn-primary w-100" disabled={isSubmitting}>{isSubmitting ? "Please wait..." : "Submit"}</button>
                            </div>
                        </div>
                    </div>

                </Form>
            )
            }
        </Formik >
    );
};

export default InputForm;