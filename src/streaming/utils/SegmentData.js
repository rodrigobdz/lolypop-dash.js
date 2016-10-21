/**
 * @author Zangue
 */ 

export default class SegmentData {
	constructor() {
		this.segments = {
			// http://130.149.49.253/dash/vod/sintel_1s/V1/1.m4s
			0: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V2/1.m4s
			1: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V3/1.m4s
			2: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V4/1.m4s
			3: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V5/1.m4s
			4: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V6/1.m4s
			5: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V7/1.m4s
			6: new Uint8Array([]),
			// http://130.149.49.253/dash/vod/sintel_1s/V8/1.m4s
			7: new Uint8Array([])
		}
	}

	get(qualityIndex) {
		if (this.segments.hasOwnProperty(qualityIndex))
			return this.segments[qualityIndex].buffer;

		return null;
	}
}