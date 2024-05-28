import BannerBackground from "../assets/home-banner-background.png";
import BannerImage from "../../public/blacky.png";
import MapaMundiPNG from "../assets/image.png"
import { NavBar } from "../components/NavBar";
import { HiArrowRight } from "react-icons/hi2";
import '../Home.css'

export function HomeWebPage() {
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
              <h1 className="primary-heading" style={{marginRight: "20px"}}>
                PollyLingo
              </h1>
              <img src={MapaMundiPNG} style={{'width': "80px"}} />
            </div>
            <p className="primary-text">
              Una plataforma emergente para el aprendizaje de idiomas
            </p>
            <button className="secondary-button">
              Registrate ahora <HiArrowRight />{" "}
            </button>
          </div>
          <div className="home-image-section">
            <img src={BannerImage} alt="" />
          </div>
        </div>
      </div>
    </div>
  );
}
