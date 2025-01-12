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
    const [game, setGame] = useState([]);

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

    // useEffect(() => {
    //     axios.get(`${apiEndpoints.url}${apiEndpoints.games.getThisGame}`)
    //         .then(res => {
    //             const returnedGames = res.data;
    //             setGame(returnedGames);
    //         })
    //         .catch(error => {
    //             toast.error(`:( Troubles With Games Loading: ${error}`);
    //         });
    // }, []);

    useEffect(() => {
        (stream?.url) ? setLoading(false)
            : setTimeout(() => {
                setLoading(false);
            }, 2000)
    }, [stream]);

    return(
        <>

            <VideoPlayer
                game={{
                    name1: "Nuggets",
                    name2: "Lakers",
                    score1: 93,
                    score2: 15,
                    logo1: "https://upload.wikimedia.org/wikipedia/ru/2/21/Denver_Nuggets.png",
                    logo2: "https://cdn.nba.com/teams/legacy/www.nba.com/lakers/sites/lakers/files/ts_180804logo.jpg"
                }}
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