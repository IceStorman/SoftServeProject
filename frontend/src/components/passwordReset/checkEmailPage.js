import { useNavigate } from "react-router-dom";
import useTranslations from "../../translationsContext";

function CheckEmailPage() {
    const navigate = useNavigate();
    const { t } = useTranslations();

    return (
        <section className="registration">
            <h2>{t("check_your_email")}</h2>
            <p>{t("reset_link_sent")}</p>
        </section>
    );
}

export default CheckEmailPage;
