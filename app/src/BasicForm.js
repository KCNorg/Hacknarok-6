import React from "react";
import { useFormik } from "formik";
import { Form, Button } from 'react-bootstrap';

const BasicForm = () => {
    // Note that we have to initialize ALL of fields with values. These
    // could come from props, but since we don’t want to prefill this form,
    // we just use an empty string. If we don’t do this, React will yell
    // at us.
    const formik = useFormik({
        initialValues: {
            firstName: "",
            email: "",
            checked: [],
        },
        onSubmit: (values) => {
            alert(JSON.stringify(values, null, 2));
        },
    });
	return (
		<Form>
			<Form.Group className="mb-3">
				<Form.Label htmlFor="firstName">First Name:</Form.Label>
				<Form.Control
					id="firstName"
					name="firstName"
					type="text"
					onChange={formik.handleChange}
					placeholder="First Name"
					value={formik.values.firstName}
					/>
			</Form.Group>

			<Form.Group className="mb-3">
				<Form.Label htmlFor="email">Email:</Form.Label>
				<Form.Control
					id="email"
					name="email"
					type="email"
					onChange={formik.handleChange}
					placeholder="Email"
					value={formik.values.email}
					/>
			</Form.Group>

			<Form.Group className="mb-3">
    			<Form.Check 
                    id="checked"
					name="checked"
					type="checkbox"
					onChange={formik.handleChange}
					value={formik.values.checked}
                    />
 			</Form.Group>

			<Button variant="primary" type="submit"> Submit </Button>
		</Form>
	)

    // return (
    //     <form onSubmit={formik.handleSubmit}>
    //         <label htmlFor="firstName">First Name</label>
    //         <input
    //             id="firstName"
    //             name="firstName"
    //             type="text"
    //             onChange={formik.handleChange}
    //             value={formik.values.firstName}
    //         />

    //         <label htmlFor="lastName">Last Name</label>
    //         <input
    //             id="lastName"
    //             name="lastName"
    //             type="text"
    //             onChange={formik.handleChange}
    //             value={formik.values.lastName}
    //         />

    //         <label htmlFor="email">Email Address</label>
    //         <input
    //             id="email"
    //             name="email"
    //             type="email"
    //             onChange={formik.handleChange}
    //             value={formik.values.email}
    //         />

    //         <Button variant="primary" type="submit"> Submit </Button>
    //     </form>
    // );
};

export default BasicForm;
