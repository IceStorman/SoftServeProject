import {useLocation, useNavigate, useParams} from "react-router-dom";
import {useEffect, useState} from "react";
import axios from "axios";
import apiEndpoints from "../apiEndpoints";
import {toast} from "sonner";
import NewsPage from "./newsPage";
import VideoPlayer from "../components/stream/videoPlayer";

function InsideStreamPage() {
    const {sportName, id} = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    const streamId = location.state || id;

    const [stream, setStream] = useState([]);

    const [loading, setLoading] = useState(false);
    //
    // useEffect(() => {
    //
    //     const fetchStreams = async () => {
    //         try {
    //             setLoading(true);
    //
    //             const response = await axios.post(
    //                 `${apiEndpoints.url}${apiEndpoints.stream.getInfo}`,
    //                 {
    //                     stream_id: streamId,
    //                 },
    //                 {
    //                     headers: {'Content-Type': 'application/json'},
    //                 }
    //             );
    //             // const fetchedStream = response.data;
    //             //
    //             // const youtubeLinks = fetchedStream.links
    //             //     .map(getYouTubeEmbedUrl)
    //             //     .filter(link => link !== null);
    //             //
    //             // const otherLinks = fetchedStream.links.filter(link => !getYouTubeEmbedUrl(link));
    //             //
    //             // setStream({
    //             //     ...fetchedStream,
    //             //     youtubeLinks,
    //             //     otherLinks,
    //             // });
    //             setStream(response.data);
    //         } catch (error) {
    //             if (stream.length === 0) {
    //                 navigate("/not-existing")
    //             }
    //             toast.error(`:( Troubles With This Stream Loading: ${error}`);
    //         }
    //     };
    //
    //     fetchStreams();
    // }, []);

    function getYouTubeEmbedUrl(url) {
        const regex = /(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})/;
        const match = url.match(regex);
        return match ? `https://www.youtube.com/embed/${match[1]}` : null;
    }

    useEffect(() => {
        (stream?.url) ? setLoading(false)
            : setTimeout(() => {
                setLoading(false);
            }, 2000)
    }, [stream]);

    return(
        <>

            <VideoPlayer
                youtubeLinks={["dQw4w9WgXcQ", "3JZ_D3ELwOQ", "UGSanw1wTlY", "UGSanw1wTlY", "UGSanw1wTlY"
                    , "UGSanw1wTlY", "UGSanw1wTlY", "UGSanw1wTlY"]}
                otherLinks={[
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                    { name: "Megogo", url: "https://partner1.com" },
                    { name: "HuiSport", url: "https://partner2.com" },
                ]}
                matchInfo={{
                    title: "Андрій робить математичний аналіз",
                    description: "Дивіться у прямому етері на те, як студент політеха страдає замість сну" +
                        ", а не спить як нормальні люди. Тільки сьгодні і тільки у нас!"
                }}
            />


    </>
    )



}
export default InsideStreamPage;