
interface IUser {
    id: number;
    username: string;

    details?: {
        email?: string;
        userClass?: string;
        accountStatus?: string;
        isDonor?: boolean;
        customTitle?: string;
        avatarUrl?: string;
        profileDescripotion?: string;
        averageSeedingSize?: string;
        ircKey?: string;
        inviteCount?: number;
        bytesUploaded?: number;
        bytesDownloaded?: number;
        lastSeeded?: string; // Date
    };
}

export default IUser;