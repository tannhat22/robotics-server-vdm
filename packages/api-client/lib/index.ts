import Debug from 'debug';
import { io, Socket } from 'socket.io-client';

const debug = Debug('rsv-client');

// https://stackoverflow.com/questions/52667959/what-is-the-purpose-of-bivariancehack-in-typescript-types
export type Listener<T = unknown> = { bivarianceHack(resp: T): void }['bivarianceHack'];
export interface Subscription {
  room: string;
  listener: Listener;
}

export class SioClient {
  public sio: Socket;
  private _subscriptions: Record<string, number> = {};

  constructor(...args: Parameters<typeof io>) {
    this.sio = io(...args);
  }

  subscribe<T>(room: string, listener: Listener<T>): Subscription {
    const subs = this._subscriptions[room] || 0;
    if (subs === 0) {
      this.sio.emit('subscribe', { room });
      debug(`subscribed to ${room}`);
    } else {
      debug(`reusing previous subscription to ${room}`);
    }
    this.sio.on(room, listener);
    this._subscriptions[room] = subs + 1;
    return { room, listener };
  }

  unsubscribe(sub: Subscription): void {
    const subCount = this._subscriptions[sub.room] || 0;
    if (!subCount) {
      debug(`tried to unsubscribe from ${sub.room}, but no subscriptions exist`);
      // continue regardless
    }
    if (subCount <= 1) {
      this.sio.emit('unsubscribe', { room: sub.room });
      delete this._subscriptions[sub.room];
      debug(`unsubscribed to ${sub.room}`);
    } else {
      this._subscriptions[sub.room] = subCount - 1;
      debug(
        `skipping unsubscribe to ${sub.room} because there are still ${subCount - 1} subscribers`,
      );
    }
    this.sio.off(sub.room, sub.listener);
  }
}

export * from './openapi';
