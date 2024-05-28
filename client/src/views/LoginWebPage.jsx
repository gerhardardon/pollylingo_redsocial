import BannerBackground from "../assets/home-banner-background.png";
import BannerImage from "../../public/blacky.png";
import { NavBar } from "../components/NavBar";
import { useState } from 'react';
import { Button, Form, Container, Row, Col } from 'react-bootstrap';
import { AlertSquare } from "../components/AlertSquare";
import { baseURL } from "../logic/constants";
import { useNavigate } from 'react-router-dom';
import Webcam from "react-webcam";
import '../Home.css'
import 'bootstrap/dist/css/bootstrap.min.css';

export function LoginWebPage() {
    let navigate = useNavigate();
    const [uploadOption, setUploadOption] = useState("credentials");
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loginStatus, setLoginStatus] = useState('null');
    const [variantStatus, setVariantStatus] = useState('');
    const [webcamRef, setWebcamRef] = useState(null);
    const [imageFile, setImageFile] = useState(null);

    const handleUsernameChange = (e) => {
        setUsername(e.target.value);
    };

    const handlePasswordChange = (e) => {
        setPassword(e.target.value);
    };


    // Handle Submit del LOGIN (Verificar Login a DB)
    const handleSubmit = async (e) => {
        e.preventDefault();




        const formData = new FormData();
        if (uploadOption === "takePicture") {
            if (!username) {
                setLoginStatus('Ingrese su username!');
                setVariantStatus('danger');
                return;
            }

            if (uploadOption === "upload" && imageFile) {
                formData.append("profilePicture", imageFile);
            } else if (uploadOption === "takePicture" && webcamRef) {
                const screenshot = webcamRef.getScreenshot();
                const blob = await fetch(screenshot).then((res) => res.blob());
                formData.append("profilePicture", blob, "profilePicture.jpg");
            } else {
                setLoginStatus("Por favor seleccione una imagen o tome una foto");
                setVariantStatus("danger");
                return;
            }

            formData.append("username", username);
            formData.append("password", "");
        } else {

            if (!username || !password) {
                setLoginStatus('Ingrese su username y su password');
                setVariantStatus('danger');
                return;
            }

            const isUserNameValid = /^[a-z0-9]+$/.test(username);
            if (!isUserNameValid) {
                setLoginStatus(
                    "El nombre de usuario solamente puede contener minúsculas y números"
                );
                setVariantStatus("danger");
                return;
            }
            formData.append("username", username);
            formData.append("password", password);
        }





        try {
            const response = await fetch(`${baseURL}/auth/login`, {
                method: 'POST',
                body: formData,
            });

            const data = await response.json();
            if (data.type == 'ok') {
                setLoginStatus('Login exitoso!');
                setVariantStatus('success');
                // Guardamos el token en localStorage para el usuario 
                //localStorage.setItem('token', data.token);
                localStorage.setItem('user', username);
                // localStorage.setItem('name', data.name)
                // viajamos a la pagina de inicio del usuario
                //history.push('/init')
                navigate('/init');


            } else {
                setLoginStatus(data.message || 'Login failed: Credenciales incorrectas');
                setVariantStatus('danger');
            }
        } catch (error) {
            setLoginStatus('Login failed: ' + error.message);
            setVariantStatus('danger');
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
                            <h1 className="primary-heading">
                                Inicio de sesión
                            </h1>
                        </div>
                        <Container>
                            <Row className="justify-content-md-left">
                                <Col md={6} className="d-flex align-items-center">
                                    <Form onSubmit={handleSubmit}>
                                        {uploadOption === "credentials" && (
                                            <>
                                                <Form.Group className="mb-3">
                                                    <Form.Label>Nombre de usuario</Form.Label>
                                                    <Form.Control type="text" required onChange={handleUsernameChange} />
                                                </Form.Group>
                                                <Form.Group className="mb-3">
                                                    <Form.Label>Contraseña</Form.Label>
                                                    <Form.Control type="password" required onChange={handlePasswordChange} />
                                                </Form.Group>
                                                <Button variant="primary" type="submit" style={{ marginBottom: "10px", display: "block" }}>Iniciar sesión</Button>
                                            </>
                                        )}


                                        <Form.Group className="mb-3">
                                            <Form.Label>Seleccione una opción:</Form.Label>
                                            <Form.Check
                                                type="radio"
                                                label="Usar mis credenciales"
                                                id="uploadOptionUpload"
                                                name="uploadOption"
                                                value="credentials"
                                                checked={uploadOption === "credentials"}
                                                onChange={() => setUploadOption("credentials")}
                                            />
                                            <Form.Check
                                                type="radio"
                                                label="Iniciar sesión con foto"
                                                id="uploadOptionTakePicture"
                                                name="uploadOption"
                                                value="takePicture"
                                                checked={uploadOption === "takePicture"}
                                                onChange={() => setUploadOption("takePicture")}
                                            />

                                        </Form.Group>
                                        {uploadOption === "takePicture" && (
                                            <>
                                                <Form.Group className="mb-3">
                                                    <Form.Label>Username</Form.Label>
                                                    <Form.Control required type="text" onChange={handleUsernameChange} />
                                                </Form.Group>

                                                <Webcam
                                                    style={{ display: "block", width: "50%" }}
                                                    audio={false}
                                                    ref={setWebcamRef}
                                                    screenshotFormat="image/jpeg"
                                                />
                                                <Button
                                                    variant="primary"
                                                    style={{ display: "block", marginBottom: "10px" }}
                                                    onClick={() => {
                                                        const isUserNameValid = username.length > 0
                                                        if (!isUserNameValid) {
                                                            setLoginStatus(
                                                                "Ingrese un nombre de usuario válido antes de tomar la foto"
                                                            );
                                                            setVariantStatus("danger");
                                                            return;
                                                        } else {
                                                            setLoginStatus(
                                                                "Foto tomada con éxito, espere..."
                                                            );
                                                            setVariantStatus("success");
                                                        }
                                                        setImageFile(webcamRef.getScreenshot());
                                                    }}
                                                    type="submit"
                                                >
                                                    Iniciar sesión con foto
                                                </Button>
                                            </>
                                        )}
                                        <a href="/register">
                                            ¿No tienes una cuenta?
                                        </a>
                                        <AlertSquare
                                            message={loginStatus}
                                            variant={variantStatus}
                                        ></AlertSquare>
                                    </Form>


                                </Col>
                                <Col md={6}>
                                </Col>


                            </Row>
                        </Container>


                    </div>
                    <div className="home-image-section">
                        <img src={BannerImage} alt="" />
                    </div>
                </div>
            </div>
        </div>
    );
}
