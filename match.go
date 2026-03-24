package main

import (
	"context"
	"database/sql"

	"github.com/heroiclabs/nakama-common/runtime"
)

type Match struct{}

type MatchState struct {
	grid [3][3]int // 0 = empty, 1 = X, 2 = O
	Players []string
	turn int
}

func (m *Match) MatchInit(ctx context.Context, logger runtime.Logger, db *sql.DB, nk runtime.NakamaModule, params map[string]interface{}) (interface{}, int, string) {

	state := &MatchState{
		grid: [3][3]int{},
		Players: []string{},
		turn: 1,
	}

	logger.Info("MatchInit called")

	return state, 1, ""
}

func (m *Match) MatchJoin(ctx context.Context, logger runtime.Logger, db *sql.DB, nk runtime.NakamaModule, state interface{}, presences []runtime.Presence) (interface{}, error) {

	gameState := state.(*MatchState)

	for _, p := range presences {
		gameState.Players = append(gameState.Players, p.GetUserId())
	}

	logger.Info("Players joined: %v", gameState.Players)

	return gameState, nil
}

func (m *Match) MatchLoop(ctx context.Context, logger runtime.Logger, db *sql.DB, nk runtime.NakamaModule, state interface{}, messages []runtime.MatchData) (interface{}, error) {

	for _, msg := range messages {
		logger.Info("Received message: %s", string(msg.GetData()))
		

		
	}
	logger.Info("MatchLoop running, messages: %d", len(messages))

	return state, nil
}

func (m *Match) MatchLeave(ctx context.Context, logger runtime.Logger, db *sql.DB, nk runtime.NakamaModule, state interface{}, presences []runtime.Presence) (interface{}, error) {
	logger.Info("Player left")
	return state, nil
}

func (m *Match) MatchTerminate(ctx context.Context, logger runtime.Logger, db *sql.DB, nk runtime.NakamaModule, state interface{}, graceSeconds int) interface{} {
	logger.Info("Match terminated")
	return state
}