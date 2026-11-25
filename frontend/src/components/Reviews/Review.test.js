import {describe, expect, it, jest, beforeEach} from "@jest/globals";
import "@testing-library/jest-dom";
import {render, screen} from "@testing-library/react";
import {MemoryRouter} from "react-router-dom";

import Review from "./Review";

jest.mock("../Common/Reactions/Review/Reaction", () => () => (
    <div data-testid={"review-reaction"}>ReviewReaction mock</div>
));

describe("Review component", () => {
    const mockReview = {
        id: 1,
        title: "test title",
        text: "test text",
        reaction: "test like",
        useful_count: 1,
        not_useful_count: 0,
        album: 1,
        type: "negative",
        updated_at: "2023-10-15T00:00:00Z",
        author: {
            avatar: "test-avatar.jpg",
            username: "test username",
        }
    }
    const albumId = 1;

    const renderComponent = (props = {}) => {
        return render(
            <MemoryRouter>
                <Review
                    review={mockReview}
                    albumId={albumId}
                    {...props}
                />
            </MemoryRouter>
        )
    }

    beforeEach(() => {
        localStorage.clear();
    });

    it('should render review components', () => {
        renderComponent();

        const avatar = screen.getByTestId("author-avatar");
        expect(avatar).toBeInTheDocument();

        const username = screen.getByTestId("author-username");
        expect(username).toBeInTheDocument();
        expect(username).toHaveTextContent("test username");

        const updated_at = screen.getByTestId("review-updated-at");
        expect(updated_at).toBeInTheDocument();
        expect(updated_at).toHaveTextContent("15 October 2023 г. 03:00");

        const title = screen.getByTestId("review-title");
        expect(title).toBeInTheDocument();
        expect(title).toHaveTextContent("test title");

        const text = screen.getByTestId("review-text");
        expect(text).toBeInTheDocument();
        expect(text).toHaveTextContent("test text");
    });

    it('should render direct ref to review if album is not equal to zero', () => {
        renderComponent();

        const direct_link = screen.getByTestId("review-direct-link-1");
        expect(direct_link).toBeInTheDocument();
    });

    it('should not render direct ref to review if album is equal to zero', () => {
        renderComponent({albumId: 0});

        const direct_link = screen.queryByTestId("review-direct-link-1");
        expect(direct_link).not.toBeInTheDocument();
    });

    it('should render ReviewReaction component if user is authenticated', () => {
        localStorage.setItem("auth_token", "some_token");
        renderComponent();

        const review_reaction = screen.getByTestId("review-reaction");
        expect(review_reaction).toBeInTheDocument();
    });

    it('should not render ReviewReaction component if user is not authenticated', () => {
        renderComponent();

        const review_reaction = screen.queryByTestId("review-reaction");
        expect(review_reaction).not.toBeInTheDocument();
    });
})