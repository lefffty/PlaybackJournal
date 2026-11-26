import {describe, expect, it, jest} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";
import AlbumSongsList from "./AlbumSongsList";

jest.mock("../Common/ScaleRating/ScaleRating", () => () => (
   <div data-testid="scale-rating"></div>
));

jest.mock("./AlbumSongsListEntry", () => () => (
    <div data-testid="album-song-list-entry"></div>
))

describe("AlbumSongsList Component", () => {
    const token = "1234";
    const album = {
        songs: [
            {id: 1, name: "test-song-name", duration: "00:03:12"},
        ]
    };
    const songsRatings = [
        {song: 1, rating: 4},
    ]
    const mockOnSongRatingChange = jest.fn();

    const renderComponent = (props = {}) => {
        return (
            render(
                <MemoryRouter>
                    <AlbumSongsList
                        album={album}
                        songsRatings={songsRatings}
                        onSongRatingChange={mockOnSongRatingChange}
                        token={token}
                    />
                </MemoryRouter>
            )
        )
    }

    beforeEach(() => {
        renderComponent();
    })

    it('should correctly render list of songs title', () => {
        const title = screen.getByTestId("album-songs-list-title");
        expect(title).toHaveTextContent("Список песен:");
    });

    it('should correctly render list of songs', () => {
        const songs = screen.getAllByTestId("album-song-list-entry");
        expect(songs.length).toBe(1);
    });
})