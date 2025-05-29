import { HiExclamationCircle } from "react-icons/hi";
import "./Notificacion.css";

const Notificacion = ( { id, temp, hum } ) =>{
    return (
        <>
            <div className="ovdrn_not">
                <div className="ovdrn_header">
                    <div className="ovdrn_l">
                        <HiExclamationCircle className="ovdrn_icon"/>
                        <p className="ovdrnh_title">ADV</p>
                    </div>
                    <div className="ovdrn_r">
                        <p className="ovdrnh_temp">{temp}°C</p>
                        <p className="ovdrnh_hum">{hum}%</p>
                    </div>
                </div>
                <div className="ovdrn_info">
                    <p className="ovdrni_title">Sensor</p>
                    <p className="ovdrni_sen">{id}</p>
                </div>
            </div>
        </>
    )
}

export default Notificacion