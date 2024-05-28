import BannerBackground from "../assets/home-banner-background.png";
import NotFoundImage from "../assets/not-found.png";
import { NavBar } from "../components/NavBar";
import { HiArrowRight } from "react-icons/hi2";
import '../Home.css'

export function NotFoundPage () {
  return (
    <div className="App">
      <div className="home-container">
        <NavBar />
        <div className="home-banner-container">
          <div className="home-bannerImage-container">
            <img src={BannerBackground} alt="" />
          </div>
          <div className="home-text-section">
            <h1 className="primary-heading">
              404: PAGINA NO ENCONTRADA
            </h1>
          </div>
          <div className="home-image-section">
            <img src={NotFoundImage} alt="" />
          </div>
        </div>
      </div>
    </div>
  );
}

