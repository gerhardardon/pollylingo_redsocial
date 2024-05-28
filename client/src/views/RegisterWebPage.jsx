import BannerBackground from "../assets/home-banner-background.png";
import BannerImage from "../../public/blacky.png";
import { NavBar } from "../components/NavBar";
import { useState } from "react";
import { Row, Col, Button, Form } from "react-bootstrap";
import { AlertSquare } from "../components/AlertSquare";
import { baseURL } from "../logic/constants";
import Webcam from "react-webcam";
import { CountryDropdown } from 'react-country-region-selector';
import "bootstrap/dist/css/bootstrap.min.css";
import '../Home.css'

export function RegisterWebPage() {
    const [username, setUsername] = useState("");
    const [fullName, setFullName] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [country, selectCountry] = useState("");
    const [uploadPicture, setUploadPicture] = useState(false);
    const [registerStatus, setregisterStatus] = useState("null");
    const [variantStatus, setVariantStatus] = useState("");
    const [imageFile, setImageFile] = useState(null);
    const [takePicture, setTakePicture] = useState(false);
    const [uploadOption, setUploadOption] = useState("upload");
    const [webcamRef, setWebcamRef] = useState(null);

    const handleImageChange = (e) => {
        const file = e.target.files[0];
        setImageFile(file);
    };

    const handleFormSubmit = async (e) => {
        e.preventDefault();

        // Validate full name
        const isFullNameValid = /^[A-Za-z\s]+$/.test(fullName);
        if (!isFullNameValid) {
            setregisterStatus(
                "El nombre completo solamente puede de contener caracteres alfabéticos"
            );
            setVariantStatus("danger");
            return;


        }


        if (fullName.length > 50) {
            setregisterStatus(
                "El nombre tiene que tener como máximo 50 caracteres"
            );
            setVariantStatus("danger");
            return;

        }

        const isUserNameValid = /^[a-z0-9]+$/.test(username);
        if (!isUserNameValid) {
            setregisterStatus(
                "El nombre de usuario solamente puede contener minúsculas y números"
            );
            setVariantStatus("danger");
            return;
        }

        if (username.length > 20 || username.length < 4) {
            setregisterStatus(
                "El nombre de usuario debe de tener de 4 a 20 caracteres"
            );
            setVariantStatus("danger");
            return;

        }

        // Validate password and confirm password
        if (password !== confirmPassword) {
            setregisterStatus("Las contraseñas no coinciden");
            setVariantStatus("danger");
            return;
        }

        // Create a FormData object and append the image file
        const formData = new FormData();
        formData.append("fullName", fullName);
        formData.append("username", username);
        formData.append("password", password);

        if (uploadPicture) {
            if (uploadOption === "upload" && imageFile) {
                formData.append("profilePicture", imageFile);
            } else if (uploadOption === "takePicture" && webcamRef) {
                const screenshot = webcamRef.getScreenshot();
                const blob = await fetch(screenshot).then((res) => res.blob());
                formData.append("profilePicture", blob, "profilePicture.jpg");
            } else {
                setregisterStatus("Por favor seleccione una imagen o tome una foto");
                setVariantStatus("danger");
                return;
            }
        }


        try {
            const response = await fetch(`${baseURL}/auth/register`, {
                method: "POST",
                body: formData,
            });
            if (response.ok) {
                const responseData = await response.json(); // Await the JSON parsing
                if (responseData.type === "err") {
                    setregisterStatus(responseData.message);
                    setVariantStatus("danger");
                } else if (responseData.type === "warning") {
                    setregisterStatus(responseData.message);
                    setVariantStatus("warning");
                } else {
                    setregisterStatus(responseData.message);
                    setVariantStatus("success");
                }
                console.log("Image uploaded successfully!");
            } else {
                setregisterStatus("Error en el servidor");
                setVariantStatus("danger");
            }
        } catch (error) {
            console.log(error);
            setVariantStatus("danger");
            setregisterStatus("Un error sucedió al subir imagen: ", error.message);
        }
    };
    return (
        <div className="App">
            <div className="home-container">
                <NavBar />
                <div className="home-banner-container">
                    <div className="home-bannerImage-container">
                        <img src={BannerBackground} style={{ "backgroundImage": '../assets/image.png', "backgroundSize": "cover" }} />
                    </div>
                    <div className="home-text-section">
                        <div style={{ display: 'flex', alignItems: 'center' }}>
                            <h1 className="primary-heading" style={{ marginRight: "20px" }}>
                                Registro
                            </h1>
                        </div>
                        {/* put here the forms again*/}
                        <Row>
                            <Col md={18} className="d-flex align-items-center">
                                <Form
                                    style={{ marginLeft: "50px", marginBottom: "5px", width: "80%", height: "95%" }}
                                    onSubmit={handleFormSubmit}
                                >
                                    <Form.Group className="mb-3" >
                                        <Form.Label htmlFor="fullName">Nombre completo</Form.Label>
                                        <Form.Control
                                            type="text"
                                            id="fullName"
                                            value={fullName}
                                            onChange={(e) => setFullName(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label htmlFor="fullName">Nombre de usuario</Form.Label>
                                        <Form.Control
                                            type="text"
                                            id="username"
                                            value={username}
                                            onChange={(e) => setUsername(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label htmlFor="password">Contraseña</Form.Label>
                                        <Form.Control
                                            type="password"
                                            id="password"
                                            value={password}
                                            onChange={(e) => setPassword(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label htmlFor="confirmPassword">
                                            Confirmar contraseña
                                        </Form.Label>
                                        <Form.Control
                                            type="password"
                                            id="confirmPassword"
                                            value={confirmPassword}
                                            onChange={(e) => setConfirmPassword(e.target.value)}
                                            required
                                        />
                                    </Form.Group>
                                    <Form.Group className="mb-3">
                                        <Form.Label htmlFor="selectCountry">
                                            País
                                        </Form.Label>
                                        <CountryDropdown
                                        id="selectCountry"
                                        value={country}
                                        onChange={selectCountry} />
                                    </Form.Group>

                                   
                                    <Form.Group className="mb-3">
                                        <Form.Check
                                            type="checkbox"
                                            label="Subir foto"
                                            onChange={() => {
                                                setUploadPicture(!uploadPicture);
                                                setTakePicture(false);
                                                setUploadOption("upload"); // Reset the uploadOption state when changing the uploadPicture state
                                            }}
                                        />
                                    </Form.Group>
                                    {/* New radio buttons for choosing between uploading and taking a picture */}
                                    {uploadPicture && (
                                        <Form.Group className="mb-3">
                                            <Form.Label>Seleccione una opción:</Form.Label>
                                            <Form.Check
                                                type="radio"
                                                label="Subir desde el ordenador"
                                                id="uploadOptionUpload"
                                                name="uploadOption"
                                                value="upload"
                                                checked={uploadOption === "upload"}
                                                onChange={() => setUploadOption("upload")}
                                            />
                                            <Form.Check
                                                type="radio"
                                                label="Tomar foto con la cámara"
                                                id="uploadOptionTakePicture"
                                                name="uploadOption"
                                                value="takePicture"
                                                checked={uploadOption === "takePicture"}
                                                onChange={() => setUploadOption("takePicture")}
                                            />
                                        </Form.Group>
                                    )}

                                    {uploadOption === "takePicture" && (
                                        <Webcam
                                            style={{ display: "block", width: "50%" }}
                                            audio={false}
                                            ref={setWebcamRef}
                                            screenshotFormat="image/jpeg"
                                        />
                                    )}
                                    {uploadOption === "takePicture" && (
                                        <Button
                                            variant="success"
                                            style={{ display: "block", marginBottom: "10px" }}
                                            onClick={() => {
                                                setImageFile(webcamRef.getScreenshot());
                                                setregisterStatus("Foto tomada correctamente, lista cuando presione 'Registrarse'");
                                                setVariantStatus("success");
                                                var iframe = "<h1>Tu foto</h1>" +
                                                    "<iframe width='100%' height='100%' src='" +
                                                    webcamRef.getScreenshot() +
                                                    "'></iframe>";
                                                var x = window.open();
                                                x.document.open();
                                                x.document.write(iframe);
                                                x.document.close();
                                            }}
                                        >
                                            Tomar foto
                                        </Button>
                                    )}

                                    {/* Conditionally render the input based on the user's choice */}
                                    {uploadPicture && !takePicture && uploadOption === "upload" && (
                                        <Form.Group className="mb-3">
                                            <Form.Label htmlFor="picture">Foto de perfil</Form.Label>
                                            <Form.Control
                                                type="file"
                                                id="image"
                                                accept="image/*"
                                                onChange={handleImageChange}
                                            />
                                        </Form.Group>
                                    )}

                                    <Button
                                        type="submit"
                                        style={{ display: "block", marginBottom: "10px" }}
                                    >
                                        Registrarse
                                    </Button>
                                    <a href="/login" style={{ display: "inline-block" }}>
                                        ¿Ya tienes una cuenta?
                                    </a>
                                    <AlertSquare
                                        message={registerStatus}
                                        variant={variantStatus}
                                    ></AlertSquare>
                                </Form>
                            </Col>
                        </Row>

                    </div>
                    <div className="home-image-section">
                        <img src={BannerImage} alt="" />
                    </div>
                </div>
            </div>
        </div>
    );
}
