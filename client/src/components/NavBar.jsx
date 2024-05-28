import Logo from "../../public/logo.png";

export function NavBar() {
  return (
    <nav>
      <div className="nav-logo-container">
        <img src={Logo} alt="" style={{"width": "70px"}} />
      </div>
      <div className="navbar-links-container">
        <a href="/">Inicio</a>
        <a href="/login">Iniciar sesión</a>
        <button className="primary-button" onClick={ () => {
          window.location.href = "/register";
        }}>Registrarme</button>
      </div>
    </nav>
  );
}
