import IRelease from './IRelease';

export interface ITorrentResponse {
    directoryName: string;
    downloadUrl: string;
    file?: { // present if isSingleFile
        name: string;
        sizeInBytes: number;
    };
    files?: { // present if !isSingleFile
        pathComponents: string[];
        sizeInBytes: number;
    }[];
    id: number;
    infoHash: string;
    isAcceptingReseedRequests: boolean;
    isApproved: boolean;
    isSingleFile: boolean;
    lastSeeded: string;
    moderatedBy: number;
    pieceSizeInBytes: number;
    release: IRelease;
    reseedRequest: any; // TODO: What is this?
    snatchCount: number;
    totalSizeInBytes: number;
    uploadedAt: string; // Date
    uploadedBy: {
        acctountStatus: string;
        avatarUrl: string;
        customTitle: string;
        id: number;
        isDonor: boolean;
        username: string;
    };
}

export interface ITorrent extends ITorrentResponse {}

// TODO: What we want to move to
export interface ITorrentIdeal {
    directoryName: string;
    downloadUrl: string;
    id: number;
    infoHash: string;
    isAcceptingReseedRequests: boolean;
    isApproved: boolean;
    isSingleFile: boolean;
    lastSeeded: string;
    moderatedBy: number;
    pieceSizeInBytes: number;
    release: IRelease;
    reseedRequest: any; // TODO: What is this?
    snatchCount: number;
    totalSizeInBytes: number;
    uploadedAt: string; // Date
    uploadedBy: number;
}

export interface ITorrentUpdate {
    infoHash: string;
    downloadUrl: string;
    filmId: number;
    cut: string; // 'Theatrical';
    codec: string; // 'XviD';
    container: string; // 'AVI';
    resolution: string; // 'Standard Def';
    sourceMedia: string; // 'DVD';
    isSource: boolean;
    is3d: boolean;
    format: string;
    uploadedBy: number;
    releaseName: string;
    releaseGroup: string;
    isScene: boolean;
    nfo: string;
    mediainfo?: {
        text: string;
        displayAspectRatio: string;
        bitRate: string;
    };
    description: string;
    comments: number[];
}

export default ITorrent;
