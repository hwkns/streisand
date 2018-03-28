
interface IUser {
    id: number;
    username: string;
    accountStatus?: string;
    avatarUrl?: string;
    customTitle?: string;
    isDonor?: boolean;
    userClass?: string;
}

export default IUser;