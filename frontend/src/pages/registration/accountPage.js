import React, {useState, useEffect, useContext} from "react";
import axios from "axios";
import {toast} from "sonner";
import globalVariables from "../../globalVariables";
import {Link, useNavigate} from "react-router-dom";
import AuthBtn from "../../components/containers/authBtn";
import useTranslations from "../../translationsContext";
import apiEndpoints from "../../apiEndpoints";
import {AuthContext, AuthProvider} from "./AuthContext";
import { Dialog } from "@headlessui/react";


function AccountPage() {
    const { t } = useTranslations();
    const authContext = useContext(AuthContext);
    const navigate = useNavigate();

    const { user, logout } = useContext(AuthContext);

    const [isOpen, setIsOpen] = useState(false);
    const handleDeleteAccount = async () => {
        setIsOpen(false);
    
        if (!user?.email) {
            toast.error("Не вдалося отримати email користувача");
            return;
        }
    
        try {
            const response = await axios.delete(apiEndpoints.deleteAccount, {
                data: { email: user.email }
            });
    
            if (response.status === 200) {
                toast.success("さようなら");
                handleLogOut();
            } else {
                toast.error("Помилка видалення акаунту");
            }
        } catch (error) {
            console.error("Помилка при видаленні акаунту:", error);
            toast.error("Сталася помилка. Спробуйте ще раз.");
        }
    };

    const handleLogOut = () => {
        logout();
        navigate(globalVariables.routeLinks.defaultRoute);
    }

    return (
            <section className="account-container registration">
                <h1 className="account-title">{t('account')}</h1>
                <div className="accountInfoContainer">
                    <div className="account-info">
                        <div className="account-row">
                            <p className="label">{t('nickname')}</p>
                            <p className="value">{user?.username}</p>
                        </div>
                        <div className="account-row">
                            <p className="label">{t('email_account')}:</p>
                            <p className="value">{user?.email}</p>
                        </div>
                    </div>
                    <div className="account-actions">
                        <button className="btn edit" onClick={()=>navigate(globalVariables.routeLinks.preferenceRoute)}>{t('change_preferences')}</button>
                        <button className="btn logout" onClick={handleLogOut}>{t('log_out')}</button>
                        <button className="btn delete" onClick={() => setIsOpen(true)}>{t('delete_account')}</button>

                        <Dialog open={isOpen} onClose={() => setIsOpen(false)} className="modal-overlay">
                            <div className="modal-content">
                                <Dialog.Title className="modal-title">{t('delete_check')}</Dialog.Title>
                                <Dialog.Description className="modal-description">
                                    {t('delete_check_text')}
                                </Dialog.Description>
                                <div className="modal-buttons">
                                    <button onClick={() => setIsOpen(false)} className="cancel-button">{t('cancel')}</button>
                                    <button onClick={handleDeleteAccount} className="confirm-button">{t('delete_account')}</button>
                                </div>
                            </div>
                        </Dialog>
                    </div>
                </div>
            </section>
    );
}

export default AccountPage;