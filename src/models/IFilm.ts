
interface IFilm {
    description: string;
    durationInMinutes: number;
    fanartUrl: string;
    id: string; // TODO: actually a number right now, need to get it changed
    imdbId: string;
    moderationNotes: string;
    posterUrl: string;
    tags: string[];
    title: string;
    tmdbId: string;
    trailerType: string;
    trailerUrl: string;
    year: number;
}

export default IFilm;