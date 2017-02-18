/* @flow */

import { Map } from 'immutable';

import type { WorkspaceState } from './model';

export const actionType = {

};

const ACTION_HANDLERS = {
};

export const actionCreator = {

};

const initialState = Map();
export const reducer = (state: WorkspaceState = initialState, action: { type: string }) => {
  const handler = ACTION_HANDLERS[action.type];
  return handler ? handler(state, action) : state;
};