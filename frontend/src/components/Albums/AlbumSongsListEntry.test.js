import {describe, expect, it, jest} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";
import userEvent from "@testing-library/user-event";

import AlbumSongsListEntry from "./AlbumSongsListEntry";

jest.mock("../Common/ScaleRating/ScaleRating", () => () => (
    <div data-testid="scale-rating"></div>
));

describe("AlbumSongsListEntry component", () => {
    const token = "1234";
    const song = {
        id: 1,
        name: "test-name",
        duration: "00:02:03",
    };
    const mockOnSongRatingChange = jest.fn();
    const songRating = 4;

    const renderComponent = (props = {}) => {
        return (
            render(
                <MemoryRouter>
                    <AlbumSongsListEntry
                        song={song}
                        onSongRatingChange={mockOnSongRatingChange}
                        songRating={songRating}
                        index={0}
                        token={token}
                        {...props}
                    />
                </MemoryRouter>
            )
        )
    }

    it('should correctly render song information', () => {
        renderComponent();

        expect(screen.getByTestId("song-index")).toHaveTextContent("1");
        expect(screen.getByTestId("song-name")).toHaveTextContent("test-name");
        expect(screen.getByTestId("song-duration")).toHaveTextContent("00:02:03");
    });

    it('should render scale rating component if user is authenticated', () => {
        renderComponent();

        expect(screen.getByTestId("scale-rating")).toBeInTheDocument();
    });

    it('should render scale rating component if user is not authenticated', () => {
        renderComponent({token: null});

        expect(screen.queryByTestId("scale-rating")).not.toBeInTheDocument();
    });
});
