
interface IFilm {
    description: string;
    duration_in_minutes: number;
    fanart_url: string;
    id: string; // TODO: actually a number right now, need to get it changed
    imdb_id: string;
    moderation_notes: string;
    poster_url: string;
    tags: string[];
    title: string;
    tmdb_id: string;
    trailer_type: string;
    trailer_url: string;
    year: number;
}

export default IFilm;