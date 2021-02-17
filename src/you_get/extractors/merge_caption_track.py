#!/usr/bin/env python
from xml.dom.minidom import parseString
from ..common import *

def time_str(time):
    m, s = divmod(time, 60); h, m = divmod(m, 60)
    return '{:0>2}:{:0>2}:{:06.3f}'.format(int(h), int(m), s).replace('.', ',')


class SrtSeg:

    def __init__(self, text):
        self.start = float(text.getAttribute('start'))
        self.dur = float(text.getAttribute('dur'))
        self.finish = (self.start + self.dur) if self.dur else (self.start + 1)
        self.content = unescape_html(text.firstChild.nodeValue)


    def start_str(self):
        return time_str(self.start)

    def finish_str(self):
        return time_str(self.finish)

    def update_with_assembled_segment(self, index, srt):
        srt.append('{}\n{} --> {}\n{}\n\n'.format(index, self.start_str(), self.finish_str(), self.content))
#        log.d('asse: {}: {}'.format(len(srt), srt[-1]))


def next_seg(track_iter):
    return SrtSeg(next(track_iter))


def merge_caption_tracks(bits_track, assembled_track):
    ''' bits_track: automatically generated caption track.
        assembled_track: Translated caption track.
        The assumption here is that the start time of each segment of the assembled_track can be found in bits_track.
        The intention for this function is to merge two tracks with the 'dur' values of the segments in bits_track fixed.
        This function refreshes the automatically generated and translated caption track seperatedly.
    '''
    srt = []
    b_index = 1
    a_index = 1
    bit = iter(bits_track)
    ait = iter(assembled_track)
    b_skip = next(bit)
    b_seg = next_seg(bit) if b_skip.firstChild is None else SrtSeg(b_skip)
    a_skip = next(ait)
    a_seg = next_seg(ait) if a_skip.firstChild is None else SrtSeg(a_skip)

    prev_b_seg = None
    prev_a_seg = None
    a_seg.update_with_assembled_segment(a_index, srt)
    srt.append('{}.{}\n{} --> '.format(a_index, b_index, b_seg.start_str()))
    b_index += 1
    prev_b_seg = b_seg
    b_seg = next_seg(bit)
    while True:
        try:
            srt.append('{}\n{}\n\n'.format(time_str(min(b_seg.start, prev_b_seg.finish)), prev_b_seg.content))
            if b_seg.start + 0.001 >= a_seg.finish:
                a_seg = next_seg(ait)
                a_index += 1
                a_seg.update_with_assembled_segment(a_index, srt)
            srt.append('{}.{}\n{} --> '.format(a_index, b_index, b_seg.start_str()))
            b_index += 1
            prev_b_seg = b_seg
            b_seg = next_seg(bit)
        except StopIteration:
            break
    srt.append('{}\n{}'.format(time_str(min(b_seg.start, prev_b_seg.finish)), prev_b_seg.content))
    return srt

