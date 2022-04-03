import React, {useState} from 'react';
import { Formik, Field, Form, useField } from 'formik';
import Select from 'react-select';
import { Multiselect } from 'multiselect-react-dropdown';
import Creatable from 'react-select/creatable'

// const sendValues = (values) => {
//     const requestOptions = {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify(values)
//     };
//     fetch('http://localhost:3000/run', requestOptions)
//     .then((response) => {
//         response.json()
//     .then((data) => {
//             console.log(data);
//         });
//     });  
// }

const InputForm = (props) => {
    const [name, setName] = useState('')
    const [family, setFamily] = useState('')
    const [age, setAge] = useState('')
    const [roleValue, setRoleValue] = useState('')
    const [tagInputValue, setTagInputValue] = useState('')
    const [tagValue, setTagValue] = useState('')
    
    
    const handleChange = (field, value) => {
      switch (field) {
        case 'roles':
          setRoleValue(value)
          break
  
        default:
          break
      }
    }
  
    const handleKeyDown = event => {
      if (!tagInputValue) return
      switch (event.key) {
        case 'Enter':
        case 'Tab':
          setTagValue([...tagValue, createOption(tagInputValue)])
          setTagInputValue('')
  
          event.preventDefault()
          break
  
        default:
          break
      }
    }
  
    const createOption = label => ({
      label,
      value: label
    })
  
    const handleInputChange = (value) => {
      setTagInputValue(value)
    }

    const data = [{Val: 'History',id:1}, {Val: 'Architecture', id:2} , {Val: 'Art', id:3}, {Val: 'Nature', id:5},{Val: 'Fun', id:5}]
    const [options] = useState(data);
    function SelectField(props) {
        const [field, state, { setValue, setTouched }] = useField(props.field.name);
        
        // value is an array now
        const onChange = (value) => {
          setValue(value);
        };
      
       // use value to make this a  controlled component
       // now when the form receives a value for 'campfeatures' it will populate as expected
        return <Select {...props} value={state?.value} isMulti onChange={onChange} onBlur={setTouched} />;
    }

    const validateForm = values => {
        const errors = {};
        if (!Number.isInteger(values.budget)) {
            errors.budget = 'Must be number';
        }


        // if (!values.email) {
        //     errors.email = 'Email is required';
        // } else if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i.test(values.email)) {
        //     errors.email = 'Invalid email address';
        // }


        // if (!values.subject) {
        //     errors.subject = 'Subject is required';
        // }

        // return errors;
    };


    return (
        <Formik
            initialValues={{ budget: '', startingplace: '', destination: '', preferences: ''}}
            onSubmit={(values, { setSubmitting }) => {
                setTimeout(() => {
                    const requestOptions = {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify(values)
                    };
                    fetch('http://localhost:3000/run', requestOptions)
                    .then((response) => {
                        response.json()
                    .then((data) => {
                            props.handler(data);
                        });
                    });
                    setSubmitting(false);

                }, 1000);
            }}
            validate={validateForm}
        >
            {(formik, isSubmitting) => (
                <Form className="row g-3">                    
                    <div className="form-group">
                        <label htmlFor="budget">Budget</label>
                        <Field placeholder='EUR' name="budget" className={(formik.touched.budget && formik.errors.budget) ? 'form-control is-invalid' : 'form-control'} type="text" />
                        
                        {formik.touched.budget && formik.errors.budget ? (
                            <div className="invalid-feedback">{formik.errors.budget}</div>
                        ) : null}
                    </div>

                    

                    <div className="form-group">
                        <label htmlFor="destination">Destination</label>
                        <Field placeholder='Example: Kraków, Poland' name="destination" className={(formik.touched.destination && formik.errors.destination) ? 'form-control is-invalid' : 'form-control'} type="text" />
                        
                        {formik.touched.destination && formik.errors.destination ? (
                            <div className="invalid-feedback">{formik.errors.destination}</div>
                        ) : null}
                    </div>

                    <div className="form-group">
                        <label htmlFor="starting-place">Length of stay</label>
                        <Field placeholder='Number of days' name="starting-place" className={(formik.touched.startingplace && formik.errors.startingplace) ? 'form-control is-invalid' : 'form-control'} type="test" />
                        
                        {formik.touched.startingplace && formik.errors.startingplace ? (
                            <div className="invalid-feedback">{formik.errors.startingplace}</div>
                        ) : null}
                    </div>

                    {/* <div className="form-group">
                        <label htmlFor="preferences">Preferences</label>
                        <Multiselect 
                         options={options}
                         displayValue="Val"
                         components={{ Option }}
                         isMulti closeMenuOnSelect={true}
                         hideSelectedOptions={true}
                         controlShouldRenderValue = { true }

                            // component={SelectField}
                            // name="campfeatures"
                            // options={selectObjects}
                        />
                    </div> */}
                    <div className="form-group">
                        <label htmlFor="preferences">Preferences</label>
                              <Creatable
                                isClearable
                                isMulti
                                components={
                                { DropdownIndicator: null }
                                }
                                options={options}
                                formatCreateLabel={() => undefined}
                                inputValue={tagInputValue}
                                menuIsOpen={false}
                                onChange={(value) => handleChange('tags', value)}
                                placeholder='Type something and press enter...'
                                onKeyDown={handleKeyDown}
                                onInputChange={handleInputChange}
                                value={tagValue}
                            />
                    </div>
                    {/* <div className="form-group">
                        <label htmlFor="subject">Subject</label>
                        <Field name="subject" className={(formik.touched.subject && formik.errors.subject) ? 'form-control is-invalid' : 'form-control'} type="text" />
                        
                        {formik.touched.subject && formik.errors.subject ? (
                            <div className="invalid-feedback">{formik.errors.subject}</div>
                        ) : null}
                    </div> */}
                    {/* <div className="form-group">
                        <label htmlFor="content">Content</label>
                        <Field name="content" className="form-control" as="textarea" rows={3} cols={10} />
                    </div> */}

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